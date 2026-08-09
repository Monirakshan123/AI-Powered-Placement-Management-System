// Dashboard Animation

const progressBars = document.querySelectorAll(".progress-fill");

window.addEventListener("load",()=>{

progressBars.forEach(bar=>{

const width = bar.style.width;

bar.style.width = "0";

setTimeout(()=>{

bar.style.width = width;

bar.style.transition = "2s";

},500);

});

});
// ==============================
// Smooth Scroll for Navbar Links
// ==============================

document.querySelectorAll('nav a[href^="#"]').forEach(link => {

    link.addEventListener("click", function(e){

        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if(target){

            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }

    });

});


// ==============================
// Role Registration Buttons
// ==============================

function studentRegister(){

    window.location.href = "/student/register/";

}

function institutionRegister(){

    window.location.href = "/institution/register/";

}

function hrRegister(){

    window.location.href = "/hr/register/";

}

function companyRegister(){

    window.location.href = "/company/register/";

}


// ==============================
// Hero Buttons
// ==============================

document.querySelector(".primary").addEventListener("click", function(){

    document.querySelector(".roles").scrollIntoView({
        behavior:"smooth"
    });

});


document.querySelector(".secondary").addEventListener("click", function(){

    window.location.href="/login/";

});


// ==============================
// Animated Statistics Counter
// ==============================

const counters = document.querySelectorAll(".counter");

const speed = 100;

counters.forEach(counter=>{

    const updateCount = ()=>{

        const target = +counter.getAttribute("data-target");

        const count = +counter.innerText;

        const increment = Math.ceil(target / speed);

        if(count < target){

            counter.innerText = count + increment;

            setTimeout(updateCount,20);

        }

        else{

            counter.innerText = target;

        }

    }

    updateCount();

});


// ==============================
// Active Navbar Highlight
// ==============================

const sections = document.querySelectorAll("section");

const navLinks = document.querySelectorAll("nav ul li a");

window.addEventListener("scroll",()=>{

    let current = "";

    sections.forEach(section=>{

        const sectionTop = section.offsetTop - 120;

        if(pageYOffset >= sectionTop){

            current = section.getAttribute("id");

        }

    });

    navLinks.forEach(link=>{

        link.classList.remove("active");

        if(link.getAttribute("href") === "#" + current){

            link.classList.add("active");

        }

    });

});
document.querySelector(".login-btn").addEventListener("click", function () {
    window.location.href = "/login/";
});