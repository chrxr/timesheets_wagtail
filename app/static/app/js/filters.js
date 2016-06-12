var filter_submit = document.getElementById('filter-submit'),
    date_submit = document.getElementById('date-submit'),
    project_filter = [document.getElementById('filter-select')],
    date_filters = [document.getElementById('date-from'),document.getElementById('date-to')]
    date_sort = document.getElementById('date-sort'),
    user_sort = document.getElementById('user-sort'),
    project_sort = document.getElementById('project-sort');

if (date_sort){
  date_sort.addEventListener('click', function(event){sortAction(event, 'date')}, false);
}

if (user_sort){
  user_sort.addEventListener('click', function(event){sortAction(event, 'user')}, false);
}

if (project_sort) {
  project_sort.addEventListener('click', function(event){sortAction(event, 'project')}, false);
}

filter_submit.addEventListener('click', function(){submitFilter(project_filter)}, false);
date_submit.addEventListener('click', function(){submitFilter(date_filters)}, false);

function sortAction(e, sort_action) {
  e.preventDefault();
  var sorter = {"name":"sort", "value":sort_action};
  submitFilter([sorter]);
}

function deconstructURL() {
  var current_url = window.location.href.split('?');
  if (current_url.length > 1){
      var filter_params = current_url[1].split('&'),
          url_params = {};
      for (var i = 0; i < filter_params.length; i++) {
        var filter = filter_params[i].split('=');
        url_params[filter[0]] = filter[1];
      }
      return url_params
  }
}

function submitProjectFilter(date_from, date_to) {
  var current_filters = deconstructURL(),
  base_url = window.location.pathname + "?";
}

function submitFilter(filters) {
  var current_filters = deconstructURL(),
      base_url = window.location.pathname + "?";
  if (current_filters) {
    for (var i = 0; i < filters.length; i++) {
      current_filters[filters[i].name] = filters[i].value;
    }
    for (var key in current_filters) {
      if (current_filters.hasOwnProperty(key)) {
        base_url = base_url + key + '=' + current_filters[key] + "&";
      }
    }
  }
  else {
    for (var i = 0; i < filters.length; i++) {
      base_url = base_url + [filters[i].name] + '=' + filters[i].value + "&";
    }
  }
  window.location.href = base_url;
}

$( "#date-from" ).datepicker(
  {dateFormat: "yy-mm-dd"}
);
$( "#date-to" ).datepicker(
  {dateFormat: "yy-mm-dd"}
);
