(function (factory) {
    if (typeof define === 'function' && define.amd) {
        define(['jquery', 'JSON', 'jquery.ui', 'jquery.ui.selectmenu', 'jquery.timeago', 'jaysun', 'myemsl.search-pager-helper', 'myemsl.search-pager'], factory);
    } else {
        factory(jQuery);
    }
}(function ($) {
    //FIXME Move this to the correct widget and pull it in via services.
    var use_cart = true;
    var history_statechanged = false;
    function myemsl_size_format(bytes) {
        var suffixes = ["B", "KB", "MB", "GB", "TB", "EB"];
        if (bytes == 0) {
            suffix = "B";
        } else {
            var order = Math.floor(Math.log(bytes) / Math.log(10) / 3);
            bytes = (bytes / Math.pow(1000, order)).toFixed(2);
            suffix = suffixes[order];
        }
        return bytes + suffix;
    }
    function myemsl_tape_status(token, item_id, cb) {
        var ajx = $.ajax({
            //FIXME foo, bar
            url: "/myemsl/item/foo/bar/" + item_id + "/2.txt/?token=" + token + "&locked",
            type: 'HEAD',
            //data: JSON.stringify(query),
            processData: false,
            //dataType: 'json',
            success: function(token, status_target) {
                return function(ajaxdata, status, xhr) {
                    var custom_header = xhr.getResponseHeader('X-MyEMSL-Locked');
                    if (custom_header == "false") {
                        cb('slow');
                    } else {
                        cb('fast');
                    }
                };
            }(token, status),
            error: function(token, status_target) {
                return function(xhr, status, error) {
                    if (xhr.status == 503) {
                        cb('slow');
                    } else {
                        cb('error');
                    }
                };
            }(token, status)
        });
        return ajx;
    }
    function cart_delete(cart_id) {
        if (cart_id == null) {
            return;
        }
        //FIXME
        var url = '/myemsl/api/2/cart';
        url += '/' + cart_id;
        $.ajax({
            url: url,
            type: 'DELETE',
            processData: false,
            dataType: 'json'
        });
    }
    function cart_submit(cart_id, email_addr) {
        if (cart_id == null) {
            return;
        }
        //FIXME
        var url = '/myemsl/api/2/cart';
        url += '/' + cart_id + '?submit&email_addr=' + email_addr;
        $.ajax({
            url: url,
            type: 'POST',
            processData: false,
            dataType: 'json'
        });
    }
    function cart_additems(data, scroll_id, count, size, total, cart_id, items, token, email_addr) {
        //FIXME
        var url = '/myemsl/api/2/cart';
        if (cart_id) {
            url += '/' + cart_id;
        }
        var ajx = $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify({
                'items': items,
                'auth_token': token
            }),
            processData: false,
            dataType: 'json',
            success: function(data, scroll_id, count, size, total, cart_id, items, token, email_addr) {
                return function(ajaxdata, status, xhr) {
                    if (!cart_id) {
                        cart_id = ajaxdata['cart_id'];
                    }
                    if (total > count) {
                        download_scan(data, scroll_id, count, size, cart_id, email_addr);
                    } else {
                        //FIXME what value here? 2 gigs for now.
                        data.download_progress_dialog.dialog('close');
                        if (size > (2 * 1000 * 1000 * 1000)) {
                            var dialog = $('<div title="Big Download"><p><span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 20px 0;"></span>You have requested to download <span class="size"></span> of files.</p><p>Do you really want to download this much data?</p></div>');
                            dialog.find('.size').text(myemsl_size_format(size));
                            dialog.dialog({
                                autoOpen: true,
                                resizable: true,
                                modal: true,
                                buttons: {
                                    "Yes": function() {
                                        cart_submit(cart_id, email_addr);
                                        $(this).dialog("close");
                                    },
                                    "Cancel": function() {
                                        cart_delete(cart_id);
                                        $(this).dialog("close");
                                    }
                                }
                            });
                        } else {
                            cart_submit(cart_id, email_addr);
                        }
                    }
                };
            }(data, scroll_id, count, size, total, cart_id, items, token, email_addr),
            error: function(data, cart_id) {
                return function(xhr, text_status, error) {
                    if (text_status != 'abort') {
                        //FIXME Better UI.
                        alert(xhr.responseText);
                        data['widget_data']['cart_cancel'] = null;
                        cart_delete(cart_id);
                    }
                };
            }(data, cart_id)
        });
        data['widget_data']['cart_cancel'] = {
            'cart_id': cart_id,
            'ajax': ajx
        };
    }
    function download_scan(data, scroll_id, count, size, cart_id, email_addr) {
        var ajx = $.ajax({
            url: data.search_url + '?auth&search_type=scan&scan',
            type: 'POST',
            data: scroll_id,
            processData: false,
            dataType: 'json',
            success: function(data) {
                return function(ajaxdata, status, xhr) {
                    var items = [];
                    for (i in ajaxdata['hits']['hits']) {
                        size += ajaxdata['hits']['hits'][i]['_source']['size'];
                        count++;
                        items.push(ajaxdata['hits']['hits'][i]['_id']);
                    }
                    data.download_progress_dialog.find(".progress").progressbar('option', 'value', count);
                    data.download_progress_dialog.find(".size").text(myemsl_size_format(size));
                    cart_additems(data, scroll_id, count, size, ajaxdata['hits']['total'], cart_id, items, ajaxdata["myemsl_auth_token"], email_addr);
                };
            }(data),
            error: function(data, cart_id) {
                return function(xhr, text_status, error_thrown) {
                    if (text_status != 'abort') {
                        //FIXME Better UI.
                        alert(xhr.responseText);
                        data['widget_data']['cart_cancel'] = null;
                        cart_delete(cart_id);
                    }
                };
            }(data, cart_id)
        });
        data['widget_data']['cart_cancel'] = {
            'cart_id': cart_id,
            'ajax': ajx
        };
    }
    function simple_items_id_url_get(id) {
        return '<a class="myemsl_iteminfo" href="/myemsl/iteminfo/' + id + '"><img src="/myemsl/static/1/moreinfo.png" alt="' + id + '"></a>';
    }
    function simple_items_file_name(subdir, file) {
        if (subdir.indexOf('/', subdir.length - '/'.length) !== - 1) {
            subdir = subdir.slice(0, subdir.length - '/'.length);
        }
        var slen = subdir.length;
        if (subdir != "") {
            file = "/" + file;
        }
        var flen = file.length;
        var choplen = 50;
        var osubdir = subdir;
        var ofile = file;
        if (slen + flen > choplen) {
            subdir = subdir.slice(0, Math.max(0, choplen - flen - 3)) + '...';
        }
        subdir = '<span class="myemsl_simple_item_subdir">' + subdir + '</span>';
        file = '<span class="myemsl_simple_item_filename">' + file + '</span>';
        return '<span title="' + osubdir + ofile + '">' + subdir + file + '</span>';
    }
    var widgets = {
        'simple_items': {
            'search_url': "/myemsl/elasticsearch/simple_items",
            'all_text': 'All Files',
            'type_desc_text': 'Files',
            'facet_desc': {
                'groups.gov_pnnl_emsl_pacifica_generic_publication': 'Publication',
                'email_addresses': 'Email Address',
                'network_ids': 'PNNL Login Name',
                'extended_metadata.gov_pnnl_emsl_instrument.name.untouched': 'Instrument Name',
                'person_names': 'First/Last Name',
                'accepted_date': 'Proposal Accepted',
                'proposals': 'Proposal Number',
                'submittername': 'Submitter Name',
                'groups.Instrument': 'Instrument ID',
                'groups.Tag': 'Keyword',
                'groups.NMR.ExperimentData': 'NMR Experiment Data',
                'groups.NWChem.CML': 'NWChem CML',
                'groups.JGI.ID': 'JGI ID',
                'groups.JGI.ftype': 'JGI File Type',
                'extended_metadata.gov_pnnl_erica/irn.id.untouched': 'Publication IRN',
                'extended_metadata.gov_pnnl_emsl_dms_datapackage.name.untouched': 'DMS Data Package',
                'extended_metadata.gov_pnnl_emsl_dms_dataset.name.untouched': 'DMS Data Set',
                'extended_metadata.gov_pnnl_emsl_dms_analysisjob.tool.name.untouched': 'DMS Analysis Tool',
                'extended_metadata.gov_pnnl_emsl_dms_analysisjob.name.untouched': 'DMS Analysis Job Name',
                'extended_metadata.gov_pnnl_emsl_dms_campaign.name.untouched': 'DMS Campaign Name',
                'extended_metadata.gov_pnnl_emsl_dms_experiment.name.untouched': 'DMS Experiment Name',
                'ext': 'Filename Extension',
                'size': 'Size Range'
            },
            'after_load': function(target, data) {
                var str = 'The requested file only exists on tape. Attempting to download this file will retrieve it from tape. This may take minutes or hours, causing download to timeout. If this happens, please try again later or contact your administrator for assistance.';
                if (use_cart == true) {
                    str = 'The requested file only exists on tape. Since downloading directly from tape can take minutes to hours, potentialy causing browser timeouts, we recommend you request the file be downloaded through a cart download request. When the file is available, you will be notified by email and will be able to download the file without delay.';
                }
                data.slow_dialog = $('<div title="Slow File"><p><span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 20px 0;"></span>' + str + '</p></div>');
                $(target).append(data.slow_dialog);
                var buttons = [
                {
                    'text': "Try Anyway",
                    'click': function() {
                        $(this).dialog("close");
                    }
                },
                {
                    'text': "Cancel",
                    'click': function() {
                        $(this).dialog("close");
                    }
                }
                ];
                if (use_cart == true) {
                    buttons.splice(0, 0, {
                        'text': 'Cart Download',
                        'click': function() {
                            $(this).dialog("close");
                        }
                    });
                }
                data.slow_dialog.dialog({
                    autoOpen: false,
                    resizable: true,
                    modal: true,
                    minWidth: 400,
                    buttons: buttons
                });
                data.download_progress_dialog = $('<div title="Building File List"><p>Building file list to download.<div class="progress"></div><div class="size"></div></div>');
                $(target).append(data.download_progress_dialog);
                data.download_progress_dialog.dialog({
                    autoOpen: false,
                    resizable: true,
                    modal: true,
                    buttons: {
                        "Cancel": function() {
                            if (data['widget_data']['cart_cancel'] != null) {
                                var obj = data['widget_data']['cart_cancel'];
                                obj['ajax'].abort();
                                cart_delete(obj['cart_id']);
                            }
                            $(this).dialog("close");
                        }
                    }
                });
                data.download_dialog = $('<div title="Download Files"><p><span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 20px 0;"></span>You have requested to download <span class="myemsl_search_count"></span> files.</p><p>Please enter the email address you would like to be contacted at when your files are ready:</p><input id="download_email_address" type="text" style="width:100%;"></div>');
                $(target).append(data.download_dialog);
                data.download_dialog.dialog({
                    autoOpen: false,
                    resizable: true,
                    modal: true,
                    buttons: {
                        "Download": function() {
                            $(this).dialog("close");
                        },
                        "Cancel": function() {
                            $(this).dialog("close");
                        }
                    }
                });
                var download = $('<button class="myemsl_search_items_download_button">Download<span class="myemsl_search_count"></span></button>');
                download.button({
                    'text': true,
                    'icons': {
                        primary: "ui-icon-transferthick-e-w"
                    }
                }).click(function(data) {
                    return function() {
                        var buttons = data.download_dialog.dialog('option', 'buttons');
                        buttons["Download"] = data['widget_data']['query_cart_download'];
                        data.download_dialog.dialog('option', 'buttons', buttons);
                        data.myemsl_search_count.text(data.myemsl_query_search_count);
                        data.download_dialog.dialog('open');
                    };
                }(data));
                if (use_cart == true) {
                    $('.myemsl_search_items_per_page').after(download);
                }
                data.download_button = download;
                data['myemsl_search_count'] = data['myemsl_search_count'].add(data.download_dialog.find('.myemsl_search_count'));
                $.ajax({
                    type: "GET",
                    url: "/myemsl/personinfo/xml",
                    success: function(data) {
                        return function(xml) {
                            $(xml).find("emailaddress").each(function() {
                                data.download_dialog.find('#download_email_address').attr('value', $(this).text());
                            });
                        };
                    }(data)
                });
            },
            'update_query': function(container, query, config) {
                config['search_url'] = config['search_url'] + '?auth';
                query["highlight"]["fields"] = {
                    "instrument_names": {},
                    "last_names": {},
                    "first_names": {},
                    "network_ids": {},
                    "email_addresses": {},
                    "title": {
                        "fragment_size": 10000
                    }
                };
                query['facets'] = {
                    "groups.gov_pnnl_emsl_pacifica_generic_publication": {
                        "terms": {
                            "field": "groups.gov_pnnl_emsl_pacifica_generic_publication.untouched"
                        }
                    },
                    "extended_metadata.gov_pnnl_erica/irn.id.untouched": {
                        "terms": {
                            "field": "extended_metadata.gov_pnnl_erica/irn.id.untouched"
                        }
                    },
                    "proposals": {
                        "terms": {
                            "field": "proposals"
                        }
                    },
                    "submittername": {
                        "terms": {
                            "field": "submittername.untouched"
                        }
                    },
                    "groups.NMR.ExperimentData": {
                        "terms": {
                            "field": "groups.NMR.ExperimentData"
                        }
                    },
                    "groups.NWChem.CML": {
                        "terms": {
                            "field": "groups.NWChem.CML"
                        }
                    },
                    "groups.JGI.ID": {
                        "terms": {
                            "field": "groups.JGI.ID"
                        }
                    },
                    "groups.JGI.ftype": {
                        "terms": {
                            "field": "groups.JGI.ftype"
                        }
                    },
                    "extended_metadata.gov_pnnl_emsl_dms_datapackage.name.untouched": {
                        "terms": {
                            "field": "extended_metadata.gov_pnnl_emsl_dms_datapackage.name.untouched"
                        }
                    },
                    "extended_metadata.gov_pnnl_emsl_dms_dataset.name.untouched": {
                        "terms": {
                            "field": "extended_metadata.gov_pnnl_emsl_dms_dataset.name.untouched"
                        }
                    },
                    "extended_metadata.gov_pnnl_emsl_dms_analysisjob.tool.name.untouched": {
                        "terms": {
                            "field": "extended_metadata.gov_pnnl_emsl_dms_analysisjob.tool.name.untouched"
                        }
                    },
                    "extended_metadata.gov_pnnl_emsl_dms_analysisjob.name.untouched": {
                        "terms": {
                            "field": "extended_metadata.gov_pnnl_emsl_dms_analysisjob.name.untouched"
                        }
                    },
                    "extended_metadata.gov_pnnl_emsl_dms_experiment.name.untouched": {
                        "terms": {
                            "field": "extended_metadata.gov_pnnl_emsl_dms_experiment.name.untouched"
                        }
                    },
                    "extended_metadata.gov_pnnl_emsl_dms_campaign.name.untouched": {
                        "terms": {
                            "field": "extended_metadata.gov_pnnl_emsl_dms_campaign.name.untouched"
                        }
                    },
                    "groups.Tag": {
                        "terms": {
                            "field": "groups.Tag"
                        }
                    },
                    "ext": {
                        "terms": {
                            "field": "ext"
                        }
                    },
                    /*          "size": {
                                "histogram": {
                                  "key_script": "log10(doc['size'].value)/3",
                                  "value_script": "1"
                                }
                              },*/
                    "size": {
                        "range" : {
                            "size" : [
                            {
                                "to" : 999
                            },
                            {
                                "to" : 999999,
                                "from" : 1000
                            },
                            {
                                "to" : 999999999,
                                "from" : 1000000
                            },
                            {
                                "from" : 1000000000
                            }
                            ]
                        }
                    },
                    "extended_metadata.gov_pnnl_emsl_instrument.name.untouched": {
                        "terms": {
                            "field": "extended_metadata.gov_pnnl_emsl_instrument.name.untouched"
                        }
                    }
                    /*
                              "accepted_date": {
                                "date_histogram" : {
                                  "field" : "accepted_date",
                                  "interval" : "year"
                                }
                              },
                              "instrument_names": {
                                "terms": {
                                  "field": "instrument_names"
                                }
                              },
                              "person_names": {
                                "terms": {
                                  "field": "person_names.untouched"
                                }
                              },
                              "network_ids": {
                                "terms": {
                                  "field": "network_ids"
                                }
                              },
                              "email_addresses": {
                                "terms": {
                                  "field": "email_addresses"
                                }
                              }
                    */
                };
            },
            'process_row': function(container, data, hit, id, ajaxres, row) {
                var suffixes = ["B", "KB", "MB", "GB", "TB", "EB"];
                var token = ajaxres["myemsl_auth_token"];
                //FIXME Token...
                var title = hit['_source']['title'];
                var widget_data = data['widget_data'];
                if (!('to_process' in widget_data)) {
                    widget_data['to_process'] = [];
                    widget_data['to_cancel'] = [];
                }
                if ('highlight' in hit && 'title' in hit['highlight']) {
                    title = hit['highlight']['title'][0];
                }
                var suffix;
                var size = hit['_source']['size'];
                if (size == 0) {
                    suffix = "B";
                } else {
                    var order = Math.floor(Math.log(size) / Math.log(10) / 3);
                    size = (size / Math.pow(1000, order)).toFixed(2);
                    suffix = suffixes[order];
                }
                var stime = hit['_source']['stime'];
                //FIXME look up icon service url.
                var icon = '/myemsl/static/1/icons/' + hit['_source']['ico'] + '.png';
                var e = $('<tr><td class="myemsl_search_simple_items_id"><img src="' + icon + '"><a class="myemsl_search_file_link" href="#">' + simple_items_file_name(hit['_source']['subdir'], hit['_source']['filename']) + '</a></td><td class="myemsl_search_simple_item_icons">' + simple_items_id_url_get(id) + '<img class="myemsl_search_simple_item_status" src="/myemsl/static/1/ajax-loader.gif"></td><td class="myemsl_simple_search_size">' + size + '</td><td class="myemsl_simple_search_size_suffix">' + suffix + '</td><td class="myemsl_search_simple_items_stime"><time class="myemsl_simple_search_time" datetime="' + stime + '">' + stime + '</time></td></tr>');

                var odd = "odd";
                if (row % 2 == 1) {
                    odd = "even";
                }
                e.find('.myemsl_iteminfo').click(function(item_id, source) {
                    return function(e) {
                        var dialog = $('<div title="Item Info"><p class="myemsl_iteminfo_data">{"test":1, "test2":[1,2,3]}</p></div>');
                        dialog.dialog({
                            autoOpen: true,
                            resizable: true,
                            modal: true,
                            position: 'center',
                            draggable: false,
                            resizable: false,
                            width: $(window).width() - 50,
                            height: $(window).height() - 50
                        });
                        //FIXME This never gets cleaned up.
                        $('.body').append(dialog);
                        //FIXME replace / with _ to work around / being in json key killing jaysun.
                        dialog.find('.myemsl_iteminfo_data').text(JSON.stringify(source, null, 4).replace('/', '_')).Jaysun({
                            collapse: true,
                            closed: false,
                            resultElement: '.myemsl_iteminfo_data'
                        });
                        e.preventDefault();
                    };
                }(id, hit['_source']));
                e.children("td").addClass('myemsl_simple_search_row_' + odd);
                e.find('.myemsl_simple_search_time').timeago();
                var l = e.find('.myemsl_search_file_link');
                l.click(function(item_id, filename, renamed_data) {
                    return function(e) {
                        var ajx = $.ajax({
                            //FIXME service file.
                            url: "/myemsl/itemauth/" + id,
                            type: 'GET',
                            processData: false,
                            dataType: "text",
                            success: function(item_id, file, slow_dialog) {
                                return function(data, status, xhr) {
                                    var server = "";
                                    //FIXME Hack around item server not working on http for now.
                                    if (window.location.href.indexOf('http://') == 0) {
                                        var tmp = window.location.href.slice('http://'.length);
                                        var idx = tmp.indexOf('/');
                                        server = 'https://' + tmp.slice(0, idx);
                                    }
                                    //FIXME foo, bar //Escape url
                                    myemsl_tape_status(data, id, function(server, id, token) {
                                        return function(state) {
                                            var cb = function() {
                                                window.location.href = server + "/myemsl/item/foo/bar/" + id + "/" + file + "?token=" + token;
                                            };
                                            if (state != "fast") {
                                                var buttons = slow_dialog.dialog('option', 'buttons');
                                                for (i in buttons) {
                                                    var button = buttons[i];
                                                    if (button['text'] == 'Try Anyway') {
                                                        button['click'] = function() {
                                                            $(this).dialog("close");
                                                            cb();
                                                        };
                                                    }
                                                    if (button['text'] == 'Cart Download') {
                                                        renamed_data.download_dialog.find('.myemsl_search_count').text('1');
                                                        button['click'] = function() {
                                                            $(this).dialog("close");
                                                            var buttons = renamed_data.download_dialog.dialog('option', 'buttons');
                                                            buttons["Download"] = function() {
                                                                cart_additems(renamed_data, null, 0, 0, 0, null, [Number(item_id)], token, renamed_data.download_dialog.find('#download_email_address').attr('value'));
                                                                renamed_data.download_dialog.dialog('close');
                                                            };
                                                            renamed_data.download_dialog.dialog('option', 'buttons', buttons);
                                                            renamed_data.download_dialog.dialog('open');
                                                        };
                                                    }
                                                }
                                                slow_dialog.dialog('option', 'buttons', buttons);
                                                slow_dialog.dialog('open');
                                            } else {
                                                cb();
                                            }
                                        };
                                    }(server, id, data));
                                };
                            }(item_id, filename, data.slow_dialog)
                        });
                        e.preventDefault();
                    };
                }(id, hit['_source']['filename'], data));
                var status = e.find('.myemsl_search_simple_item_status');
                //status.hide();
                widget_data['to_process'].push([id, status]);
                //        var l = $('<a href="#">' + id + '</a>');
                //        l.click(function(data, id) { return function(e) {
                //          data.proposal_clicked(id);
                //          e.preventDefault();
                //        }}(data, id));
                //        e.find('.myemsl_search_proposal_id').append(l);
                return e;
            },
            'display_facets_update': function(display_facets, data) {
                display_facets.sort(function(a, b) {
                    //Prioritize based on hard coded values first.
                    var weights = {
                        'proposals': 1000,
                        'size': 0
                    };
                    var wa = weights[a.id];
                    var wb = weights[b.id];
                    if (!wa) {
                        wa = 50;
                    }
                    if (!wb) {
                        wb = 50;
                    }
                    if (wa != wb) {
                        return (wa < wb);
                    }
                    //If the same weight, prioritize down incomplete facet lists.
                    if (a.other != b.other) {
                        return (a.other > b.other);
                    }
                    //All else being equal, prioritize based on text name.
                    return data.facet_desc[a.id] > data.facet_desc[b.id];
                });
                var count = 0;
                //Handle removing facet content that wont fit.
                for (var i = 0; i < display_facets.length; i++) {
                    count++;
                    var facet = display_facets[i];
                    count += facet.list.length;
                    if (count > 30) {
                        if (facet.id == 'size') {
                            display_facets.splice(i, 1);
                            i--;
                        } else {
                            facet.other += facet.list.length;
                            facet.list = [];
                        }
                    }
                }
            },
            'process_done': function(container, data, hit, query) {
                var token = hit["myemsl_auth_token"];
                var widget_data = data['widget_data'];
                if (data['myemsl_search_count'].eq(0).text() == '0') {
                    data.download_button.button('disable');
                } else {
                    data.download_button.button('enable');
                }
                if ('slow_timer' in widget_data) {
                    window.clearTimeout(widget_data['slow_timer']);
                }
                if ('to_process' in widget_data) {
                    widget_data['slow_timer'] = setTimeout(function(container, data, to_process) {
                        return function() {
                            for (var i in widget_data.to_cancel) {
                                widget_data.to_cancel[i].abort();
                            }
                            widget_data.to_cancel = [];
                            for (var i in to_process) {
                                var id = to_process[i][0];
                                var status = to_process[i][1];
                                var ajx = myemsl_tape_status(token, id, function(status) {
                                    return function(state) {
                                        if (state != "fast") {
                                            status.attr('src', '/myemsl/static/1/turtle.png');
                                        } else {
                                            status.hide();
                                        }
                                    };
                                }(status));
                                widget_data['to_cancel'].push(ajx);
                            }
                        };
                    }(container, data, widget_data['to_process']), 500);
                    widget_data['to_process'] = [];
                }
                widget_data['query_cart_download'] = function(data, query) {
                    return function() {
                        data.download_dialog.dialog("close");
                        data.download_progress_dialog.find(".progress").progressbar({
                            value: 0,
                            max: 1
                        });
                        data.download_progress_dialog.dialog("open");
                        var newquery = {
                            query: $.extend({}, query['query'])
                        };
                        $.ajax({
                            url: data.search_url + '?search_type=scan',
                            type: 'POST',
                            data: JSON.stringify(newquery),
                            processData: false,
                            dataType: 'json',
                            success: function(ajaxdata, status, xhr) {
                                data.download_progress_dialog.find(".progress" ).progressbar('option', 'max', ajaxdata['hits']['total']);
                                download_scan(data, ajaxdata['_scroll_id'], 0, 0, null, data.download_dialog.find('#download_email_address').attr('value'));
                            }
                        });
                    };
                }(data, query);
            }
        },
        'proposal': {
            'search_url': "/myemsl/elasticsearch-raw/myemsl_current_proposal/proposal/_search",
            'all_text': 'All Proposals',
            'type_desc_text': 'Proposals',
            'facet_desc': {
                'email_addresses': 'Email Address',
                'network_ids': 'PNNL Login Name',
                'extended_metadata.gov_pnnl_emsl_instrument.name.untouched': 'Instrument Names',
                'person_names': 'First/Last Name',
                'accepted_date': 'Proposal Accepted'
            },
            'update_query': function(container, query) {
                query["highlight"]["fields"] = {
                    "instrument_names": {},
                    "last_names": {},
                    "first_names": {},
                    "network_ids": {},
                    "email_addresses": {},
                    "title": {
                        "fragment_size": 10000
                    }
                };
                query['facets'] = {
                    "accepted_date": {
                        "date_histogram" : {
                            "field" : "accepted_date",
                            "interval" : "year"
                            //            "range" : {
                            //              "accepted_date" : [
                            //                {
                            //                   "to" : (year - 2).toString() + "-01-01"
                            //                },
                            //                {
                            //                  "to" : (year - 1).toString() + "-12-31",
                            //                  "from" : (year - 2).toString() + "-01-01"
                            //                },
                            //                  {
                            //                    "to" : year.toString() + "-12-31",
                            //                    "from" : (year - 1).toString() + "-01-01"
                            //                  },
                            //                  {
                            //                    "from" : year.toString() + "-01-01"
                            //                  }
                            //                ]
                            //              } 

                        }
                    },
                    "instrument_names": {
                        "terms": {
                            "field": "instrument_names"
                        }
                    },
                    "person_names": {
                        "terms": {
                            "field": "person_names.untouched"
                        }
                    },
                    "network_ids": {
                        "terms": {
                            "field": "network_ids"
                        }
                    },
                    "email_addresses": {
                        "terms": {
                            "field": "email_addresses"
                        }
                    }
                };
            },
            'process_row': function(container, data, hit, id) {
                var title = hit['_source']['title'];
                if ('highlight' in hit && 'title' in hit['highlight']) {
                    title = hit['highlight']['title'][0];
                }
                var e = $('<tr><td class="myemsl_search_proposal_id"></td><td>' + title + '</td></tr>');
                var l = $('<a href="#">' + id + '</a>');
                l.click(function(data, id) {
                    return function(e) {
                        data.proposal_clicked(id);
                        e.preventDefault();
                    };
                }(data, id));
                e.find('.myemsl_search_proposal_id').append(l);
                return e;
            }
        },
        'unit': {
            'all_text': 'All Units',
            'type_desc_text': 'Units',
            'search_url': '/myemsl/elasticsearch-raw/myemsl_unit_index_1346084652/unit/_search',
            'facet_desc': {
                'type': 'Catagory of Unit',
                'mods_name': 'Scale Modifier'
            },
            'update_query': function(container, query) {
                query["highlight"]["fields"] = {
                    "type": {},
                    "mods_name": {}
                };
                query['facets'] = {
                    "type": {
                        "terms": {
                            "field": "type.untouched"
                        }
                    },
                    "mods_name": {
                        "terms": {
                            "field": "mods_name",
                            "size": 20,
                            "order": "term"
                        }
                    }
                };
            },
            'process_row': function(container, data, hit, id) {
                var type = hit['_source']['type'];
                var symb = hit['_source']['symb'];
                var title = hit['_source']['namep'];
                var e = $('<tr><td class="myemsl_search_proposal_id"></td><td>' + title + '</td></tr>');
                var l = $('<a href="#">' + symb + '</a>');
                l.click(function(data, id, type, namep) {
                    return function(e) {
                        data.proposal_clicked({
                            'key': namep,
                            'val': id,
                            'type': type
                        });
                        e.preventDefault();
                    };
                }(data, id, type, title));
                e.find('.myemsl_search_proposal_id').append(l);
                return e;
            },
            'after_load': function(target, data) {
                var marker = $('<div style="width: 100%; height: 100%; overflow: auto"/>').insertBefore(target);
                target.detach();
                marker.append(target);
                //target.height('200px');
                target.height('100%');
                //        target.css('margin-bottom', '200px');
                target.parent().css('padding-bottom', '1em');
                //      target.parent().css('margin-bottom', '100px');
                target.parent().css('-moz-box-sizing', 'border-box');
                target.parent().css('-webkit-box-sizing', 'border-box');
                target.parent().css('box-sizing', 'border-box');
                target.css('overflow', 'auto');
                //        target.height('400px');
                //        target.css('overflow', 'auto');
                var section = $('<span style="position: absolute; bottom: 0px;"><span style="vertical-align:middle; width: 16px; height: 16px; display: inline-block" class="ui-icon ui-icon-alert"></span> If you can not find the unit you need after searching, you can enter a place holder unit by clicking <a href="#">here</a>.</span>');
                section.find('a').click(function(target, data) {
                    return function (e) {
                        e.preventDefault();
                        var dialog = $('<div title="Place Holder Unit Entry"><p>Please note, that using a place holder unit will make it difficult to search for your data based on this value. Use an existing type whenever possible and only use a place holder only when an alternative does not exist.</p><p>Please enter a name for the Unit of Measure.</p><input style="width: 100%;" type="text" size="10"></p>');
                        dialog.dialog({
                            resizable: false,
                            height: 210,
                            modal: true,
                            buttons: {
                                "Ok": function() {
                                    var name = dialog.find('input').val();
                                    //FIXME add blank error check.
                                    //                alert(name);
                                    data.proposal_clicked({
                                        'key': name,
                                        'val': '(unknown:' + name + ')',
                                        'type': 'unknown'
                                    });
                                    $(this).dialog("close");
                                },
                                Cancel: function() {
                                    $(this).dialog("close");
                                }
                            }
                        });
                        dialog.scrollTop(0);
                    };
                }(target, data));
                target.parent().parent().append(section);
                //        target.parent().parent().parent().bind("dialogresize", function(target) { return function(event, ui) {
                //          //console.log(target.parent().parent().height());
                //          console.log("resized");//target.parent().parent().height());
                //        }}(target));
            }
        },
        'predicate': {
            'search_url': "/myemsl/elasticsearch-raw/myemsl_local_predicate_index_1347305073/local_predicate/_search",
            'all_text': 'All Predicates',
            'type_desc_text': 'Predicates',
            'facet_desc': {
                'submitter.name': 'First/Last Name'
            },
            'update_query': function(container, query) {
                query['facets'] = {
                    "submitter.name": {
                        "terms": {
                            "field": "submitter.name.untouched"
                        }
                    }
                };
            },
            'process_row': function(container, data, hit, id) {
                if (container.find('.myemsl_search_results').children().length <= 0) {
                    container.find('.myemsl_search_results').prepend('<tr><th>ID</th><th>Submitter</th><th>Shot Description</th><th></th></tr>');
                }
                var title = hit['_source']['description']['short'];
                var e = $('<tr><td class="myemsl_search_id"></td><td>' + hit['_source']['submitter']['name'] + '</td><td>' + title + '</td><td><span class="button"/>&nbsp;</td></tr>');
                var l = $('<a href="#">' + id + '</a>');
                l.click(function(data, id) {
                    return function(e) {
                        data.proposal_clicked({
                            'key': hit['_source']['description']['short'],
                            'val': id
                        });
                        e.preventDefault();
                    };
                }(data, id));
                e.find('.myemsl_search_id').append(l);
                e.find('.button').button({
                    'text': false,
                    'icons': {
                        primary: "ui-icon-search"
                    }
                }).click(function(hit) {
                    return function() {
                        alert(hit['_source']['description']['long']);
                    };
                }(hit));
                return e;
            },
            'after_load': function(target, data) {
                var marker = $('<div style="width: 100%; height: 100%; overflow: auto"/>').insertBefore(target);
                target.detach();
                marker.append(target);
                target.height('100%');
                target.parent().css('padding-bottom', '1em');
                target.parent().css('-moz-box-sizing', 'border-box');
                target.parent().css('-webkit-box-sizing', 'border-box');
                target.parent().css('box-sizing', 'border-box');
                target.css('overflow', 'auto');
                var section = $('<span style="position: absolute; bottom: 0px;"><span style="vertical-align:middle; width: 16px; height: 16px; display: inline-block" class="ui-icon ui-icon-alert"></span> If you can not find the tag type you need after searching, you can create a new one by clicking <a href="#">here</a>.</span>');
                section.find('a').click(function(target, data) {
                    return function (e) {
                        e.preventDefault();
                        //FIXME need a callback....
                        window.myemslLocalPredicateWizard.show();
                    };
                }(target, data));
                target.parent().parent().append(section);
            }
        }
    };
    var methods = {
        init: function(options) {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('myemslProposalFinderForm');
                if (!data) {
                    var data = {
                        target: $this,
                        proposal: null,
                        'type_desc_text': "Results",
                        'update_query': null,
                        'search_url': "/myemsl/simple/_search",
                        'layout_url': "/myemsl/api/1/elasticsearch/generic-finder-layout.html",
                        'facet_desc': {},
                        'all_text': "All",
                        'process_row': function(container, data, hit, id) {
                            var e = $('<tr><td class="myemsl_search_proposal_id"></td></tr>');
                            var l = $('<a href="#">' + id + '</a>');
                            l.click(function(data, id) {
                                return function(e) {
                                    data.proposal_clicked(id);
                                    e.preventDefault();
                                };
                            }(data, id));
                            e.find('.myemsl_search_proposal_id').append(l);
                            return e;
                        },
                        'display_facets_update': function(display_facets, data) {
                            display_facets.sort(function(a, b) {
                                return data.facet_desc[a.id] > data.facet_desc[b.id]
                            });
                        },
                        'process_done': null,
                        'after_load': null,
                        facets_set: [],
                        facets_updated: false,
                        search_counter: 0,
                        search_counter_res: 0,
                        widget_data: {},
                        force_refresh: 0,
                        page: 0,
                        old_page: 0,
                        old_query: null,
                        state_save: false,
                        proposal_clicked: function($this) {
                            return function(id) {
                                var data = $this.data('myemslProposalFinderForm');
                                data.proposal = id;
                                data.target.trigger('myemsl_proposal_changed');
                            };
                        }($this)
                    };
                    if ('widget' in options) {
                        if (options['widget'] in widgets) {
                            $.extend(data, widgets[options['widget']]);
                        }
                    }
                    $.extend(data, options);
                    $(this).data('myemslProposalFinderForm', data);
                    data = $this.data('myemslProposalFinderForm');
                    $this.load(data.layout_url, function(data, $this) {
                        return function () {
                            data['myemsl_search_pager'] = $this.find('.myemsl_search_pager');
                            data['myemsl_search'] = $this.find('.myemsl_search');
                            data['myemsl_search_selected_facets'] = $this.find('.myemsl_search_selected_facets');
                            data['myemsl_search_facets'] = $this.find('.myemsl_search_facets');
                            data['myemsl_search_results'] = $this.find('.myemsl_search_results');
                            var search_items_per_page = $this.find('.myemsl_search_items_per_page');
                            search_items_per_page.wrap('<span class="myemsl_search_items_per_page"></span>');
                            search_items_per_page.removeClass('myemsl_search_items_per_page');
                            search_items_per_page.selectmenu({
                                //data.myemsl_search_items_per_page.change(function() {
                                change: function() {
                                    $this.myemslProposalFinderForm('force_refresh');
                                    $this.myemslProposalFinderForm('focus_search_text_box');
                                }
                            });
                            //});
                            data['myemsl_search_items_per_page'] = search_items_per_page;
                            data['myemsl_search_count'] = $this.find('.myemsl_search_count');
                            $this.find('.myemsl_search_type_desc').html(data.type_desc_text);
                            data.myemsl_search.on('paste keyup input', function() {
                                $this.myemslProposalFinderForm('update_form');
                            });
                            $this.myemslProposalFinderForm('focus_search_text_box');
                            $(document).ready(function() {
                                $this.myemslProposalFinderForm('update_form');
                            });
                            data['myemsl_search_pager'].myemslSearchPager({
                                'switch_page': function($this, data) {
                                    return function(page) {
                                        $this.myemslProposalFinderForm('switch_page', page - 1);
                                    };
                                }($this, data)
                            });
                            if (data.after_load) {
                                data.after_load($this, data);
                            }
                        };
                    }(data, $this));
                }
            });
        },
        destroy: function() {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('myemslProposalFinderForm');
                $(window).unbind('.myemslProposalFinderForm');
                $this.removeData('myemslProposalFinderForm');
            });
        },
        focus_search_text_box: function() {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('myemslProposalFinderForm');
                data.myemsl_search.focus();
            });
        },
        facet_link_set: function(args) {
            var facet = args.facet;
            var term = args.term;
            var query_term = args.query_term;
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('myemslProposalFinderForm');
                var a = {
                    'facet': facet,
                    'term': term,
                    'query_term': query_term
                };
                data.facets_set.push(a);
                data.facets_updated = true;
                $this.myemslProposalFinderForm('update_form');
                $this.myemslProposalFinderForm('focus_search_text_box');
            });
        },
        facet_link_remove: function(args) {
            var facet = args.facet;
            var term = args.term;
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('myemslProposalFinderForm');
                for (var i in data.facets_set) {
                    if (data.facets_set[i]['facet'] == facet && data.facets_set[i]['term'] == term) {
                        data.facets_set.splice(i, 1);
                        data.facets_updated = true;
                        break;
                    }
                }
                $this.myemslProposalFinderForm('update_form');
                $this.myemslProposalFinderForm('focus_search_text_box');
            });
        },
        facet_link_remove_to: function(args) {
            var facet = args.facet;
            var term = args.term;
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('myemslProposalFinderForm');
                for (var i in data.facets_set) {
                    if (data.facets_set[i]['facet'] == facet && data.facets_set[i]['term'] == term) {
                        data.facets_set.splice(i + 1, data.facets_set.length - i - 1);
                        data.facets_updated = true;
                        break;
                    }
                }
                $this.myemslProposalFinderForm('update_form');
                $this.myemslProposalFinderForm('focus_search_text_box');
            });
        },
        proposal: function() {
            var proposal = null;
            this.each(function() {
                var $this = $(this);
                var data = $this.data('myemslProposalFinderForm');
                proposal = data.proposal;
            });
            return proposal;
        },
        select: function(item) {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('myemslProposalFinderForm');
                data.proposal_clicked(item);
            });
        },
        force_refresh: function() {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('myemslProposalFinderForm');
                data.force_refresh = 1;
                $this.myemslProposalFinderForm('update_form_dont_reset_page');
            });
        },
        switch_page: function(page) {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('myemslProposalFinderForm');
                data.old_page = data.page;
                data.page = page;
                $this.myemslProposalFinderForm('update_form_dont_reset_page');
            });
        },
        update_form: function() {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('myemslProposalFinderForm');
                $this.myemslProposalFinderForm('switch_page', 0);
            });
        },
        update_form_dont_reset_page: function() {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('myemslProposalFinderForm');
                var target = data.target;
                var v = data.myemsl_search.val();
                var s = "";
                for (var i in data.facets_set) {
                    var query_term = data.facets_set[i]['query_term'];
                    s += " " + query_term;
                }
                v += s;
                if (v == "") {
                    v = "*";
                }
                if (data.force_refresh == 0 && v == data.old_query && data.old_page == data.page) {
                    return;
                } else {
                    data.old_query = v;
                    data.force_refresh = 0;
                }
                state = {
                    'facets_set': data.facets_set,
                    'facets_updated': data.facets_updated,
                    'text_search': data.myemsl_search.val()
                };
                if (window.history.pushState && data.state_save) {
                    var replace = false;
                    if (window.history.state)
                    {
                        var oldstate = window.history.state;
                        if (oldstate.facets_updated == false && data.facets_updated == false) {
                            replace = true;
                        }
                    }
                    if (replace) {
                        window.history.replaceState(state, '', '');
                    } else {
                        window.history.pushState(state, '', '');
                    }
                } else if (!window.history.pushState && data.state_save) {
                    history_statechanged = true;
                }
                data.facets_updated = false;
                data.state_save = true;
                /*FIXME This is really not the place for this. */
                window.onbeforeunload = function() {
                    if (history_statechanged) {
                        return "The history support in your web browser is broken. If you just hit the back button intending to undo some search criteria, you may unexpectedly loose your place if you continue. You may want to upgrade your browser to an HTML 5 comparable browser to ensure optimum functionality for this application. Are you sure you want to navigate away from this page?";
                    }
                };
                onpopstate = function(event) {
                    if (event.state) {
                        data.facets_set = event.state.facets_set;
                        data.myemsl_search.val(event.state.text_search);
                    } else {
                        data.facets_set = [];
                        data.myemsl_search.val('');
                    }
                    data.state_save = false;
                    $this.myemslProposalFinderForm('force_refresh');
                };
                if (data.facets_set.length > 0) {
                    data.myemsl_search_selected_facets.html('');
                } else {
                    var text = data.all_text;
                    if (v === undefined || v.length > 0) {
                        text = "Text Search";
                    }
                    data.myemsl_search_selected_facets.html('<div class="myemsl_search_selected_facets_row"><span class="myemsl_search_selected_facet_name">' + text + '</span><span class="myemsl_search_selected_facet_remove myemsl_search_selected_facet_remove_link">&nbsp;</span></div>');
                }
                for (var i in data.facets_set) {
                    var facet = data.facets_set[i]['facet'];
                    var term = data.facets_set[i]['term'];
                    var more = "";
                    if (i > 0) {
                        more = "<span> &gt; </span>";
                    }
                    var e = $(more + '<span class="myemsl_search_selected_facets_row"><span class="myemsl_search_selected_facet_name"></span> <span class="myemsl_search_selected_facet_remove"></span></span>');
                    var l = $('<a href="#" class="myemsl_search_selected_facet_link">' + data.facet_desc[facet] + " : " + term + '</a>');
                    l.click(function(target, facet, term) {
                        return function(e) {
                            e.preventDefault();
                            target.myemslProposalFinderForm('facet_link_remove_to', {
                                'facet': facet,
                                'term': term
                            });
                        };
                    }(target, facet, term));
                    var l2 = $('<a href="#" class="myemsl_search_selected_facet_remove_link">(X)</a>');
                    l2.click(function(target, facet, term) {
                        return function(e) {
                            e.preventDefault();
                            target.myemslProposalFinderForm('facet_link_remove', {
                                'facet': facet,
                                'term': term
                            });
                        };
                    }(target, facet, term));
                    e.find('.myemsl_search_selected_facet_name').append(l);
                    e.find('.myemsl_search_selected_facet_remove').append(l2);
                    data.myemsl_search_selected_facets.append(e);
                }
                var date = new Date();
                var year = date.getFullYear();
                var query = {
                    "query": {
                        "bool": {
                            "must": [
                            {
                                "query_string": {
                                    "default_operator": "AND",
                                    "default_field": "_all",
                                    "query": v
                                }
                            }
                            ],
                            "must_not": [],
                            "should": []
                        }
                    },
                    "highlight": {
                        "number_of_fragments": 3,
                        "fragment_size": 20
                    },
                    "from": data.page * data.myemsl_search_items_per_page.val(),
                    "size": data.myemsl_search_items_per_page.val(),
                    "sort": []
                };
                var config = {
                    'search_url': data.search_url
                };
                if (data.update_query != null) {
                    data.update_query($this, query, config);
                }
                data['search_counter'] += 1;
                (function(data, search_counter_id, query, config) {
                    $.ajax({
                        url: config['search_url'],
                        type: 'POST',
                        data: JSON.stringify(query),
                        processData: false,
                        dataType: 'json',
                        success: function(ajaxdata, status, xhr) {
                            if (search_counter_id > data['search_counter_res']) {
                                data['search_counter_res'] = search_counter_id;
                            } else {
                                return;
                            }
                            data.myemsl_search_results.text('');
                            data.myemsl_search_facets.text('');
                            data.myemsl_search_count.text(ajaxdata['hits']['total']);
                            data.myemsl_query_search_count = ajaxdata['hits']['total'];
                            //FIXME unhardcode
                            data['myemsl_search_pager'].myemslSearchPager('update_pager', ajaxdata['hits']['total'], data.myemsl_search_items_per_page.val(), data.page + 1, 9);
                            var hits = ajaxdata['hits']['hits'];
                            for (var i in hits) {
                                var hit = hits[i];
                                var id = hit['_id'];

                                var row = data.process_row(data.target, data, hit, id, ajaxdata, i);
                                if (row != null) {
                                    data.myemsl_search_results.append(row);
                                }
                            }
                            var facets = ajaxdata['facets'];
                            var display_facets = [];
                            for (var i in facets) {
                                var facet = facets[i];
                                var count = 0;
                                var region = 'terms';
                                if (facet['_type'] == 'date_histogram') {
                                    region = 'entries';
                                    facet[region].reverse();
                                } else if (facet['_type'] == 'histogram') {
                                    region = 'entries';
                                } else if (facet['_type'] == 'range') {
                                    region = 'ranges';
                                }
                                for (var j in facet[region]) {
                                    if (region == 'ranges') {
                                        if (facet[region][j]['count'] != 0) {
                                            count++;
                                        }
                                    } else if (region == 'terms') {
                                        if (facet[region][j]['count'] != ajaxdata['hits']['total']) {
                                            count++;
                                        }
                                    } else {
                                        count++;
                                    }
                                }
                                if (count < 2 && (facet['total'] < 1 || facet['missing'] < 1)) {
                                    continue;
                                }
                                //FIXME make style better.
                                var display_facet = {
                                    'id': i,
                                    'title': $('<span class="myemsl_search_facet_title">' + data.facet_desc[i] + '</span>'),
                                    'text_title': data.facet_desc[i],
                                    'list': []
                                };
                                var sizes = {
                                    0: "B",
                                    1: "KB",
                                    2: "MB",
                                    3: "GB"
                                };
                                for (var j in facet[region]) {
                                    var term;
                                    var query_term;
                                    var count = facet[region][j]['count'];
                                    if (facet['_type'] == 'date_histogram') {
                                        if (j > 5) {
                                            break;
                                        }
                                        var year = new Date(facet[region][j]['time']).getFullYear() + 1;
                                        term = year;
                                        query_term = i + ':[\"' + year.toString() + '-01-01\" TO \"' + year.toString() + '-12-31\"]';
                                    } else if (facet['_type'] == 'histogram') {
                                        var size = facet[region][j]['key'];
                                        term = size;
                                        query_term = i + ':[\"' + size.toString();
                                    } else if (facet['_type'] == 'range') {
                                        if ('from_str' in facet[region][j]) {
                                            term = new Date(facet[region][j]['from_str']).getFullYear();
                                            query_term = 'FIXME';
                                        } else {
                                            var c = facet[region][j]['count'];
                                            if (c == 0 || c == ajaxdata['hits']['total']) {
                                                continue;
                                            }
                                            if (j >= 3) {
                                                term = ">= 1 GB";
                                                query_term = i + ':[ ' + facet[region][j]['from'] + ' TO * ]';
                                            } else {
                                                if (j < 1) {
                                                    term = '0 - 999' + sizes[j];
                                                    query_term = i + ':[ * TO ' + facet[region][j]['to'] + ']';
                                                } else {
                                                    term = '1 - 999' + sizes[j];
                                                    query_term = i + ':[' + facet[region][j]['from'] + ' TO ' + facet[region][j]['to'] + ']';
                                                }
                                            }
                                        }
                                    } else {
                                        term = facet[region][j]['term'];
                                        query_term = i + ':\"' + term + '\"';
                                    }
                                    var e = $('<div class="myemsl_search_facet_row"><span class="myemsl_search_facet_name"></span> <span class="myemsl_search_gray_count">(' + count + ')</span></div>');
                                    var l = $('<a href="#" class="myemsl_search_facet_link">' + term + '</a>');
                                    l.click(function(target, facet, term, query_term) {
                                        return function(e) {
                                            e.preventDefault();
                                            target.myemslProposalFinderForm('facet_link_set', {
                                                'facet': facet,
                                                'term': term,
                                                'query_term': query_term
                                            });
                                        };
                                    }(target, i, term, query_term));
                                    e.find('.myemsl_search_facet_name').append(l);
                                    display_facet['list'].push(e);
                                }
                                display_facet['other'] = facet['other'];
                                if (display_facet['list'].length != 0) {
                                    display_facets.push(display_facet);
                                }
                            }
                            data.display_facets_update(display_facets, data);
                            for (var i in display_facets) {
                                var display_facet = display_facets[i];
                                data.myemsl_search_facets.append(display_facet['title']);
                                for (var j in display_facet['list']) {
                                    data.myemsl_search_facets.append(display_facet['list'][j]);
                                }
                                //FIXME put an upper bound on what count we allow here.
                                var MAXFACETENTRIES = 10000;
                                if (display_facet['other'] > 0) {
                                    var ddd = $('<div class="myemsl_search_facet_row" style="font-size:75%"><a href="#" class="myemsl_search_facet_ddd">[more]</a></div>');
                                    ddd.click(function(data, display_facet) {
                                        return function(e) {
                                            var facetquery = jQuery.extend(true, {}, {
                                                'query': query['query'],
                                                'size': 1,
                                                'facets': {}
                                            });
                                            facetquery['facets'][display_facet.id] = query['facets'][display_facet.id];
                                            for (var i in facetquery['facets']) {
                                                var facet = facetquery['facets'][i];
                                                for (var j in facet) {
                                                    var type = facet[j];
                                                    type['size'] = MAXFACETENTRIES;
                                                }
                                            }
                                            //FIXME make throbber not hardcoded.
                                            //FIXME unhardcode style
                                            var dialog = $('<div title="' + display_facet.text_title + '"><p style="max-height: 200px" class="content">Loading... <img src="/myemsl/static/1/ajax-loader.gif"></p></div>');
                                            var content = dialog.find('.content');
                                            dialog.dialog({
                                                autoOpen: true,
                                                resizable: true,
                                                modal: true
                                            });
                                            $.ajax({
                                                url: config['search_url'],
                                                type: 'POST',
                                                data: JSON.stringify(facetquery),
                                                processData: false,
                                                dataType: 'json',
                                                success: function(ajaxdata, status, xhr) {
                                                    var input = $('<input class="myemsl_search_facet_search" type="text" name="search">');
                                                    content.html('');
                                                    content.append(input);
                                                    var rows = {}
                                                    var facets = ajaxdata['facets'];
                                                    for (var i in facets) {
                                                        var facet = facets[i];
                                                        //FIXME unhardcode these things. functionaize the facet engine code above and share.
                                                        var region = 'terms';
                                                        for (var j in facet[region]) {
                                                            //FIXME use different style here for better overridability.
                                                            var term = facet[region][j].term;
                                                            var query_term = display_facet.id + ':\"' + term + '\"';
                                                            var e = $('<div class="myemsl_search_facet_row"><span class="myemsl_search_facet_name"></span><span class="myemsl_search_gray_count"> (' + facet[region][j].count + ')</span></div>');
                                                            var l = $('<a href="#" class="myemsl_search_facet_link">' + term + '</a>');
                                                            l.click(function(target, facet, term, query_term) {
                                                                return function(e) {
                                                                    e.preventDefault();
                                                                    target.myemslProposalFinderForm('facet_link_set', {
                                                                        'facet': facet,
                                                                        'term': term,
                                                                        'query_term': query_term
                                                                    });
                                                                    dialog.dialog('close');
                                                                };
                                                            }(target, display_facet.id, term, query_term));
                                                            e.find('.myemsl_search_facet_name').append(l);
                                                            rows[term] = e;
                                                            content.append(e);
                                                            input.focus();
                                                        }
                                                    };
                                                    input.keyup(function() {
                                                        var val = input.val();
                                                        for (var i in rows) {
                                                            if (i.indexOf(val) != - 1) {
                                                                rows[i].show();
                                                            } else {
                                                                rows[i].hide();
                                                            }
                                                        }
                                                    });
                                                }
                                            });
                                            e.preventDefault();
                                        };
                                    }(data, display_facet));
                                    data.myemsl_search_facets.append(ddd);
                                }
                            }
                            /*FIXME need a work around for it not supporting long lines
                                          data.target.tooltip({
                                            tooltipClass:'myemsl_search_simple_item_tooltip'

                                            content: function() {
                                              var element = $(this);
                                              return '<div style="cwhite-space:nowrap">' + element.attr("title") + '</div>';
                                            }

                                          });
                            */
                            if (data.process_done) {
                                data.process_done(data.target, data, ajaxdata, query);
                            }
                        }
                    });
                })(data, data['search_counter'], query, config);
            });
        }
    };
    $.fn.myemslProposalFinderForm = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.myemslProposalFinderForm');
        }
    };
}));


