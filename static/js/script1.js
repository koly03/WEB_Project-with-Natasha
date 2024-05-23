
document.addEventListener('DOMContentLoaded', (event) => {
    const burgerMenu = document.querySelector('.burger-menu');
    const imgElement = document.querySelector('img'); 
    const newImgSrc = '/static/img/cross.png';
    const oldImgSrc = '/static/img/menu.png';
    const burger = document.querySelector('.burger');

    if(burgerMenu && burger) {
        burgerMenu.addEventListener('click', () => {
            if (burger.classList.contains('active')) {
                burgerMenu.classList.remove('active');
                burger.classList.remove('active');
                imgElement.src = oldImgSrc;
            } else {
                burgerMenu.classList.add('active');
                burger.classList.add('active');
                imgElement.src = newImgSrc;
            }
        });
    } else {
        console.log('Elements not found');
    }
});


function addOther(n) {
    document.querySelector('#'+n).insertAdjacentHTML("beforebegin", "<li style=\"list-style-type: none\">" +
        "<input type=\"text\" name=\""+ n +"[]\" placeholder=\"Ecrire...\"/> </li>");
}

// function addOther(n) {
//     document.querySelector(n).insertAdjacentHTML("beforebegin", "<li style=\"list-style-type: none\">" +
//         "<input type=\"text\" name=\"newG\" placeholder=\"Ecrire...\"/> </li>");
// }
