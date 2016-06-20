mobile_menu_button = document.getElementById('mobile-menu-button');
mobile_menu_container = document.getElementById('mobile-menu-container')

mobile_menu_button.addEventListener('click', function(){revealMenu(mobile_menu_container);},false);

function revealMenu(menu) {
  // classes = menu.getAttribute('class');
  // classes = classes.split(' ');
  // console.log(classes);
  if (menu.classList.contains('menu-open')){
    menu.classList.remove("menu-open");
  }
  else {
    menu.classList.add("menu-open");
  }
}
