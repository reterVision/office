var filter1 = {name: "Email", url:"http://api.laliza.com/members", list:[], action:"search_by_email"};
filter1.list.push({name:"email",type:"text",required:true});
var filter2 = {name: "List", url:"http://api.laliza.com/members", list:[], action:"list_email"};
// filter2.list.push({name:"email_provider",type:"option", data:"activecampaign,madmimi", defaults:"madmimi"});
filter2.list.push({name:"start",type:"uint", defaults: "0"});
filter2.list.push({name:"limit",type:"uint"});
var filters = [filter1, filter2];

$(document).ready(function(){
	initFilter({"searchbar":"#data_view_searchbar", "table":"#data_view_table", "filters":filters});
});

function initFilter(options){
	var selectedFilters = 0;

	var $searchbar = $(options.searchbar);
	var $table = $(options.table);
	var str = "<select class='main'>";
	for(var i = 0; i < options.filters.length; i++){
		str += "<option value='"+i+"'>"+options.filters[i].name+"</option>"
	}
	str += "</select>";
	str += "<button class='btn btn-info search'>Search</button>";
	$searchbar.html(str).find("select.main").on("change", function(){
		selectedFilters = $(this).val();
		renderSearchFilterList(options.filters[selectedFilters].list);
	});
	$searchbar.find("button.search").on("click", function(){
		$searchbar.find("div.search-list.no-"+selectedFilters).find("form").submit();
		// var str = "?"
		// var obj = options.filters[selectedFilters];
		// var params = obj.list;
		// for(var i = 0; i < params.length; i++){
		// 	var $div = $searchbar.find("div.search-list.no-"+selectedFilters);
		// 	var value = $div.find("*[name='"+params[i].name+"']").val();
		// 	// TODO MIAO: check input here
		// 	if(value == "" && params[i].required == true){
		// 			alert(params[i].name+" is needed.");
		// 			return;
		// 	}else if(value != ""){
		// 		str += params[i].name+"="+value+"&";
		// 	}
			
		// }
		// $.ajax({url: (obj.url+str), 
		// 		type: "GET", 
		// 		crossDomain: true, 
		// 		dataType: "jsonp",
		// 		success: function(response) {
		// 			//console.log(response.data);
		// 		}
		// 	});
	});

	renderSearchFilterList(options.filters[selectedFilters].list);

	function renderSearchFilterList(filterList){
		if($searchbar.find("div.search-list.no-"+selectedFilters).length > 0){
			$searchbar.find("div.search-list").hide().filter(".no-"+selectedFilters).show();
			return;
		}
		var action = options.filters[selectedFilters].action;
		var str = "<div class='search-list no-"+selectedFilters+"'>";
		str += '<form enctype="multipart/form-data" method="POST" action="/data_view">'
		for(var i = 0; i < filterList.length; i++){
			var singleFilter = filterList[i];
			var name = singleFilter.name;
			var defaults = singleFilter.defaults ? singleFilter.defaults : "";
			str += "<lable>"+name+": </label>";
			switch(singleFilter.type){
				case "uint":
					str += "<input min='0' type='number' name='"+name+"' value='"+defaults+"'/>"
					break;
				case "option":
					str += "<select name='"+name+"'>";
					var arr = singleFilter.data.split(",");
					for(var j = 0; j < arr.length; j++){
						if(defaults == arr[j]){
							str += "<option value='"+arr[j]+"' selected='selected'>"+arr[j]+"</option>";
						}else{
							str += "<option value='"+arr[j]+"'>"+arr[j]+"</option>";
						}
					}
					str += "</select>";
					break;
				case "text":
					str += "<input type='text' name='"+name+"' value='"+defaults+"'/>"
					break;
			}
		}
		str += "<input type='hidden' name='action' value='"+ action +"'>"
		str += "</form></div>";
		$searchbar.find("button.search").before($(str));
		$searchbar.find("div.search-list").hide().filter(".no-"+selectedFilters).show();
	}

	function isInt(value){
		return ((parseInt(value, 10) + "") == value);
	}
	function isUint(value){
		var uint = parseInt(value, 10);
		return ((uint + "") == value && uint >= 0);
	}
}