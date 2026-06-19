require 'bibtex'

# Computes publication statistics from the jekyll-scholar bibliography and
# exposes them as `site.data['pub_stats']` for rendering on the publications page.
#
# Classification rules. An EXPLICIT per-entry flag always wins; a text marker is
# only a convenience fallback so already-tagged entries keep working. To count a
# paper unambiguously, add one (or more) of these custom BibTeX fields:
#   - scie  = {true}   -> SCIE/SCI journal               (fallback: text has "JCR")
#   - bk21  = {true}   -> NRF BK21+ recognised venue      (fallback: text has "BK21")
#   - kiise = {true}   -> KIISE-CS recognised venue       (fallback: text has "KIISE-CS")
# These three categories are independent; a paper may set more than one.
#   - recent 5y / 3y : counted by publication `year` relative to build time and
#             limited to papers in the SCIE / BK21 / KIISE-CS categories above;
#             a per-year breakdown is exported so the page can recompute the
#             rolling windows live in the browser.
module Jekyll
  class PublicationStatsGenerator < Generator
    safe true
    priority :low

    def generate(site)
      scholar  = site.config['scholar'] || {}
      source   = (scholar['source'] || '/_bibliography/').sub(%r{^/}, '')
      bib_name = scholar['bibliography'] || 'papers.bib'
      path     = File.join(site.source, source, bib_name)

      current_year = Time.now.year
      stats = {
        'total' => 0, 'scie' => 0, 'bk' => 0, 'kiise' => 0,
        'by_year' => {}, 'current_year' => current_year,
        'recent5' => 0, 'recent3' => 0,
        'recent5_from' => current_year - 4,
        'recent3_from' => current_year - 2
      }

      begin
        bib = BibTeX.open(path)
        bib.entries.each_value do |e|
          stats['total'] += 1

          flag    = ->(key) { e[key].to_s.strip.downcase == 'true' }
          present = ->(key) { v = e[key].to_s.strip; !v.empty? && v.downcase != 'false' }

          haystack  = [e['journal'], e['booktitle'], e['note']].map(&:to_s).join(' ')
          is_scie   = flag.call('scie')  || present.call('jcr_if')  || haystack =~ /JCR/i
          is_bk     = flag.call('bk21')  || flag.call('bk') || present.call('bk21_if') || haystack =~ /BK21/i
          # `kiise` now carries a grade value (우수/최우수); any non-empty value counts.
          is_kiise  = present.call('kiise') || flag.call('kiise_cs') || haystack =~ /KIISE-CS/i

          stats['scie']  += 1 if is_scie
          stats['bk']    += 1 if is_bk
          stats['kiise'] += 1 if is_kiise

          # Recent-year tallies cover only SCIE / BK21 / KIISE-CS publications.
          next unless is_scie || is_bk || is_kiise

          year = e['year'].to_s.gsub(/[^0-9]/, '')
          next if year.empty?

          yi = year.to_i
          stats['by_year'][yi] = (stats['by_year'][yi] || 0) + 1
          stats['recent5'] += 1 if yi >= current_year - 4
          stats['recent3'] += 1 if yi >= current_year - 2
        end
      rescue => ex
        Jekyll.logger.warn 'PublicationStats:', "could not parse #{path}: #{ex.message}"
      end

      site.data['pub_stats'] = stats
    end
  end
end
