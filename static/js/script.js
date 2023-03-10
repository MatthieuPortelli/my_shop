// --- ALERT ---
setTimeout(function() {
    bootstrap.Alert.getOrCreateInstance(document.querySelector("#message")).close();
}, 3000)

// --- COOKIE ---
let cookieModal = document.querySelector(".cookie-consent-modal")
let cancelCookieBtn = document.querySelector(".btn.cancel")
let acceptCookieBtn = document.querySelector(".btn.accept")

cancelCookieBtn.addEventListener("click", function (){
    cookieModal.classList.remove("active")
    localStorage.setItem("cookieAccepted", "no")
})

acceptCookieBtn.addEventListener("click", function (){
    cookieModal.classList.remove("active")
    localStorage.setItem("cookieAccepted", "yes")
})

setTimeout(function (){
    let cookieAccepted = localStorage.getItem("cookieAccepted")
    if (cookieAccepted != "yes" && cookieAccepted != "no"){
        cookieModal.classList.add("active")
    }
}, 2000)
