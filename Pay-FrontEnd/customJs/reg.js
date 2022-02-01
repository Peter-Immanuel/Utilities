// Event listeners
document.getElementById("continueBtn").addEventListener('click', regPage2)
document.getElementById("backBtn").addEventListener('click', regPage1)
document.getElementById('name').addEventListener("input", validateName)



function regPage2(){
        document.getElementById('contentPage1').style.display='none'
        document.getElementById('contentPage2').style.display='flex'
        document.getElementById('regPage1').style.display= "none"
        document.getElementById('regPage2').style.display= "flex"
}

function regPage1() {
        document.getElementById('contentPage1').style.display = 'flex'
        document.getElementById('contentPage2').style.display = 'none'
        document.getElementById('regPage1').style.display = "flex"
        document.getElementById('regPage2').style.display = "none"
}

function validateName(){
        let name = document.getElementById('name')
        let img = document.createElement('img')
        if (name == 'peter'){
                img.src = "/img/SVG icons/done_black_18dp.svg"
        }else{
                img.src="/img/SVG icons/highlight_off_black_18dp.svg"
        }
        img.id='nameField'
        document.getElementById("nameField").replaceWith(img)
        console.log(name.value)
}



