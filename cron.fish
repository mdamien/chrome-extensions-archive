function mesay
      cowsay $argv | lolcat;
      date | lolcat;
end


while true
	mesay crawl_sitemap;
	p crawl_sitemap.py;
	mesay crawl_crx;
	p crawl_crx.py;
	mesay scan_pages_history_to_big_list;
	p scan_pages_history_to_big_list.py;
	mesay crx_stats;
	p crx_stats.py;
	mesay make_site;
	p make_site.py
end

