var app = angular.module("AuthApp", []);

app.controller("AuthController",) 
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

document.addEventListener("DOMContentLoaded", function () {
    let likeCount = localStorage.getItem("likeCount") || 0;
    document.getElementById("likeCount").innerText = likeCount;
});
let itemID = "product-123"; // Unique ID
let likeKey = `likeCount-${itemID}`;

function handleLike() {
    let likeCount = localStorage.getItem("likeCount") || 0;
    likeCount = parseInt(likeCount) + 1;
    
    localStorage.setItem("likeCount", likeCount);
    document.getElementById("likeCount").innerText = likeCount;
}

 localStorage.setItem("cart", JSON.stringify([
    { image: "images/hd1.jpg", price: "₹999", days: "3 days", quantity: 2 },
    { image: "images/hd2.jpg", price: "₹499", days: "1 day", quantity: 1 }
  ]));
  
  
  $http.post("http://127.0.0.1:5000/submit", {
    name: name,
    phone: phone
})
.then(response => {
    console.log(response.data.message);
    localStorage.setItem("username", name);
})
.catch(error => {
    alert("Error: " + error);
});

  
fetch("/update-profile", {
  method: "POST",
  body: formData
})

let isLiked = false;
let likeCount = 0;

function toggleLike() {
    const heartIcon = document.getElementById("heartIcon");
    const likeDisplay = document.getElementById("likeCount");

    if (!isLiked) {
        isLiked = true;
        likeCount++;
        heartIcon.innerText = "❤️"; // filled heart
    } else {
        isLiked = false;
        likeCount--;
        heartIcon.innerText = "🤍"; // empty heart
    }

    likeDisplay.innerText = likeCount;
}
