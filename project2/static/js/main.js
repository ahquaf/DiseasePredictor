// scroll nav
window.onscroll = function () { scrollFunction() };
function scrollFunction() {
    var navLink = document.getElementsByClassName("nav-link");
    var hex = document.getElementsByClassName("hex");
    var width = $(window).width();
    console.log(width);
    if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
        document.getElementById("navbar").style.background = "#fff";
        document.getElementById("navbar").style.boxShadow = "0 0 5px grey";
        document.getElementById("brand-image").style.filter = "invert(0)";
        for (var i = 0; i < navLink.length; i++) {
            if (width > 800) {
                navLink[i].style.color = "#363636";
            }
            hex[i].style.backgroundColor = "black";
            hex[i].style.opacity = "0.05";
        }
        document.getElementById("toggle-icon").style.filter = "invert(0)";
    } else {
        document.getElementById("navbar").style.background = "none";
        document.getElementById("navbar").style.boxShadow = "none";
        document.getElementById("brand-image").style.filter = "invert(1)";
        for (var i = 0; i < navLink.length; i++) {
            if (width > 800) {
                navLink[i].style.color = "#fff";
            }
            hex[i].style.backgroundColor = "white";
            hex[i].style.opacity = "0.2";
        }
        document.getElementById("toggle-icon").style.filter = "invert(1)";
    }
}

// explore us button animation
const buttons = document.querySelectorAll('.explore');
buttons.forEach(btn => {
    btn.addEventListener('mouseenter', function (e) {
        let ripples = document.createElement('span');
        this.appendChild(ripples);
        setTimeout(() => {
            ripples.remove();
        }, 1000);
    })
});

// fireworks
$('.firework').fireworks({
    sound: false, // sound effect
    opacity: 0.8,
    height: '100%',
    // width: '100%'
});

// slider
$('.brand-slider').slick({
    dots: false,
    infinite: true,
    slidesToShow: 5,
    slidesToScroll: 5,
    autoplay: true,
    autoplaySpeed: 3000,
    prevArrow: ".slider-btn.prev",
    nextArrow: ".slider-btn.next",
    responsive: [
        {
            breakpoint: 1200,
            settings: {
                slidesToShow: 4,
                slidesToScroll: 4,
                infinite: true,
                dots: true
            }
        },
        {
            breakpoint: 800,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 3
            }
        },
        {
            breakpoint: 500,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 2
            }
        }
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
    ]
});

$(document).ready(function () {
    // joinUs Form
    $("#joinUs").submit(function (event) {
        event.preventDefault();

        // getting values from form
        var fname = $("#fname").val();
        var lname = $("#lname").val();
        var address = $("#address").val();
        var state = $("#state").val();
        var city = $("#city").val();
        var zipcode = $("#zipcode").val();
        var mobileNo = $("#mobileNo").val();
        var email = $("#email").val();
        var jobType = $("#jobType").val();
        var submit = $("#submit").val();

        $(".form-message").load("./php/joinUs.php", {
            // syntax -> postName : variableName
            fname: fname,
            lname: lname,
            address: address,
            state: state,
            city: city,
            zipcode: zipcode,
            mobileNo: mobileNo,
            email: email,
            jobType: jobType,
            submit: submit
        });
        setTimeout(this, 1000);
    });
});

$(document).ready(function () {
    // artist join us form
    $("#artistjoin").submit(function (event1) {
        event1.preventDefault();
        // getting values from form
        var fname1 = $("#fname1").val();
        var lname1 = $("#lname1").val();
        var socialMedia1 = $("#socialMedia1").val();
        var art1 = $("#art1").val()
        var address1 = $("#address1").val()
        var state1 = $("#state1").val();
        var city1 = $("#city1").val();
        var zipcode1 = $("#zipcode1").val();
        var mobileNo1 = $("#mobileno1").val();
        var email1 = $("#email1").val();
        var portfolio1 = $("#portfolio1").val();
        var submit1 = $("#submit1").val();
        $(".form-message1").load("./php/artistJoinUs.php", {
            // syntax -> postName : variableName
            fname1: fname1,
            lname1: lname1,
            socialMedia1: socialMedia1,
            art1: art1,
            address1: address1,
            state1: state1,
            city1: city1,
            zipcode1: zipcode1,
            mobileno1: mobileNo1,
            email1: email1,
            portfolio1: portfolio1,
            submit1: submit1
        });
    });
});

$(document).ready(function () {
    // sponsorship form
    $("#sponsor").submit(function (event1) {
        event1.preventDefault();
        // getting values from form
        var ename = $("#ename").val();
        var edesc = $("#edesc").val();
        var estart = $("#estart").val();
        var eend = $("#eend").val()
        var eloc = $("#eloc").val()
        var email3 = $("#email3").val();
        var esubmit = $("#esubmit").val();
        $(".form-message2").load("./php/sponsorship.php", {
            // syntax -> postName : variableName
            ename: ename,
            edesc: edesc,
            estart: estart,
            eend: eend,
            eloc: eloc,
            email3: email3,
            esubmit: esubmit
        });
    });
});