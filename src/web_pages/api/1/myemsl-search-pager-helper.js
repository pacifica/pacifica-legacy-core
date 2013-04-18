function myemsl_paginate_subparts(greatest_page, current_page, adj_page_width) {
        var half_page_width = Math.floor(adj_page_width/2);
        var start = current_page - half_page_width;
        var end = current_page + half_page_width;

	if(start < 1) {
		end = Math.min(adj_page_width, greatest_page);
		start = 1;
	}
	else {
		if(end > greatest_page) {
			start = greatest_page - adj_page_width + 1;
			end = greatest_page;
		}
		start = Math.max(start, 1);
		if(end - start + 1 > adj_page_width) {
			end--;
		}
	}
	var pages = []
	for(var i = start; i <= end; i++) {
	        pages.push(i);
	}
	return pages;
}

function myemsl_paginate_parts(count, per_page, current_page, page_width) {
        var greatest_page = 1;
        if(count > per_page) {
                greatest_page = Math.ceil(count/per_page);
        }
        var adj_page_width = Math.min(page_width, greatest_page);
	return {'pager': myemsl_paginate_subparts(greatest_page, current_page, adj_page_width), 'current':current_page, 'greatest_page':greatest_page};
	
}
