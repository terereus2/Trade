

let colect = document.querySelectorAll('div');

let newDiv = document.createElement('div')
    newDiv.className = 'add-div'
    document.body.appendChild(newDiv)

let redBtn = document.querySelector('.red')
let blackBtn = document.querySelector('.black')

index = colect.length-1

redBtn.addEventListener('click', () => {
    colect[index].style.display = 'none';
    let secondDiv = document.querySelector(".add-div");
    colect[index].classList.add('colect-img')
    secondDiv.appendChild(colect[index]);
    index--

    let cardsRedOrBlack = secondDiv.lastElementChild
    let className = cardsRedOrBlack.className;

    if(className =='hearts start colect-img' || className == 'diamonds start colect-img'){
        let inputRed = document.querySelector('.red-value');
        let currentValue = parseInt(inputRed.value);
    if(isNaN(currentValue)){
        inputRed.value = 0;
        }
     let newValue = parseInt(inputRed.value) + 1;
     inputRed.value = newValue;
    }

})


blackBtn.addEventListener('click', () => {
    colect[index].style.display = 'none';
    let secondDiv = document.querySelector(".add-div");
    colect[index].classList.add('colect-img')
    secondDiv.appendChild(colect[index]);
    index--

    let cardsRedOrBlack = secondDiv.lastElementChild
    let className = cardsRedOrBlack.className;

    if(className =='spades start colect-img' || className == 'clubs start colect-img'){
        let inputRed = document.querySelector('.black-value');
        let currentValue = parseInt(inputRed.value);
    if(isNaN(currentValue)){
        inputRed.value = 0;
    }
    let newValue = parseInt(inputRed.value) + 1;
    inputRed.value = newValue;
    }
})















