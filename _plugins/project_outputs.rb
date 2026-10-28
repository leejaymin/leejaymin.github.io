require 'bibtex'

# Links publications to research projects (사사 관리) and exposes them for rendering.
#
# Sources
#   - International papers : jekyll-scholar bibliography; add `projects = {key1, key2}`.
#                            @article -> 국제저널, @inproceedings -> 국제학회.
#   - Domestic / patents   : _data/domestic_pubs.yml; add `projects: [key1, key2]`.
#   - Projects             : _research/*.md front matter `key`, `grant_no`, `ack_ko`, `ack_en`.
#
# Exposed data
#   - site.data['project_outputs'][key] : [{id, label, count, years: [{year, items}]}]
#                                         (non-empty categories only, years descending)
#   - site.data['outputs_ledger']       : every output with year >= ACK_FROM_YEAR, for /outputs/
#
# Outputs from ACK_FROM_YEAR onward without `projects` (or with an unknown key) are
# reported as build warnings so missing acknowledgements are caught early.
module Jekyll
  class ProjectOutputsGenerator < Generator
    safe true
    priority :low

    ACK_FROM_YEAR = 2026
    CATEGORIES = [
      %w[intl_journal 국제저널],
      %w[intl_conf 국제학회],
      %w[domestic_journal 국내저널],
      %w[domestic_conf 국내학회],
      %w[patent_applied 특허출원],
      %w[patent_granted 특허등록]
    ].freeze

    def generate(site)
      @site     = site
      projects  = {}
      (site.collections['research']&.docs || []).each do |doc|
        key = doc.data['key'].to_s.strip
        next if key.empty?
        projects[key] = { 'key' => key, 'title' => doc.data['title'], 'url' => doc.url }
      end

      items = bib_items + domestic_items
      items.each do |it|
        it['projects'] = it['project_keys'].map { |k| projects[k] || { 'key' => k, 'title' => k, 'url' => nil } }
        next if it['year'] < ACK_FROM_YEAR
        if it['project_keys'].empty?
          Jekyll.logger.warn 'ProjectOutputs:', "사사 과제 미기재 (#{it['year']}) #{it['label']}: #{plain(it['title'])[0, 60]}"
        end
        (it['project_keys'] - projects.keys).each do |k|
          Jekyll.logger.warn 'ProjectOutputs:', "알 수 없는 project key '#{k}': #{plain(it['title'])[0, 60]}"
        end
      end

      outputs = {}
      projects.each_key do |key|
        mine = items.select { |it| it['project_keys'].include?(key) }
        outputs[key] = CATEGORIES.filter_map do |id, label|
          cat = mine.select { |it| it['category'] == id }
          next if cat.empty?
          years = cat.group_by { |it| it['year'] }.sort_by { |y, _| -y }
                     .map { |y, list| { 'year' => y, 'items' => list } }
          { 'id' => id, 'label' => label, 'count' => cat.size, 'years' => years }
        end
      end

      order = CATEGORIES.map(&:first)
      site.data['project_outputs'] = outputs
      site.data['outputs_ledger']  = items.select { |it| it['year'] >= ACK_FROM_YEAR }
                                          .sort_by { |it| [-it['year'], order.index(it['category'])] }
    end

    private

    def bib_items
      scholar = @site.config['scholar'] || {}
      source  = (scholar['source'] || '/_bibliography/').sub(%r{^/}, '')
      path    = File.join(@site.source, source, scholar['bibliography'] || 'papers.bib')
      bib     = BibTeX.open(path, parse_names: false)
      bib.entries.each_value.map do |e|
        e = e.convert(:latex) rescue e
        journal = e.type.to_s == 'article'
        {
          'category'     => journal ? 'intl_journal' : 'intl_conf',
          'label'        => journal ? '국제저널' : '국제학회',
          'title'        => plain(e['title']),
          'authors'      => e['author'].to_s.split(/\s+and\s+/).map { |a| bold_me(a.strip) }.join(', '),
          'venue'        => plain(journal ? e['journal'] : e['booktitle']),
          'abbr'         => e['abbr'].to_s,
          'award'        => e['award'].to_s,
          'year'         => e['year'].to_s.gsub(/\D/, '').to_i,
          'url'          => bib_url(e),
          'project_keys' => keys(e['projects'].to_s)
        }
      end
    rescue => ex
      Jekyll.logger.warn 'ProjectOutputs:', "could not parse #{path}: #{ex.message}"
      []
    end

    def domestic_items
      (@site.data['domestic_pubs'] || []).map do |d|
        type = d['type'].to_s
        it = {
          'title'        => d['title'].to_s,
          'authors'      => d['authors'].to_s,
          'url'          => d['url'].to_s,
          'award'        => d['badge'].to_s,
          'abbr'         => '',
          'project_keys' => keys(d['projects'])
        }
        if type == 'patent'
          granted = d['status'].to_s == 'granted'
          no, date = granted ? [d['reg_no'], d['reg_date']] : [d['app_no'], d['app_date']]
          it['category'] = granted ? 'patent_granted' : 'patent_applied'
          it['label']    = granted ? '특허등록' : '특허출원'
          it['venue']    = "#{d['country'] || 'KR'} #{granted ? '등록' : '출원'} #{no} (#{date})"
          it['year']     = (date.to_s[/\d{4}/] || d['year']).to_i
        else
          it['category'] = type
          it['label']    = type == 'domestic_journal' ? '국내저널' : '국내학회'
          it['venue']    = d['venue'].to_s
          it['year']     = d['year'].to_i
        end
        it
      end
    end

    def keys(value)
      list = value.is_a?(Array) ? value : value.to_s.split(/[,;\s]+/)
      list.map { |k| k.to_s.strip }.reject(&:empty?)
    end

    def plain(text)
      text.to_s.gsub(/[{}]/, '').gsub(/\s+/, ' ').strip
    end

    def bold_me(name)
      me = "#{@site.config.dig('scholar', 'first_name')} #{@site.config.dig('scholar', 'last_name')}"
      name.start_with?(me) ? "<strong>#{name}</strong>" : name
    end

    def bib_url(e)
      pdf = e['pdf'].to_s
      return pdf if pdf.include?('://')
      return "/assets/pdf/#{pdf}" unless pdf.empty?
      return e['html'].to_s unless e['html'].to_s.empty?
      return "https://doi.org/#{e['doi']}" unless e['doi'].to_s.empty?
      ''
    end
  end
end
