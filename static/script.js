let user_id = Math.floor(Math.random() * 1000000); // oddiy identifikator
let count = 0;

document.getElementById("logo").addEventListener("click", () => {
    fetch("/click", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `user_id=${user_id}`
    })
    .then(res => res.json())
    .then(data => {
        count = data.coins;
        document.getElementById("count").innerText = `Tangalar: ${count}`;
    });
});

document.getElementById("wallet-btn").addEventListener("click", () => {
    document.getElementById("wallet").classList.toggle("hidden");
});

document.getElementById("withdraw").addEventListener("click", () => {
    const address = document.getElementById("address").value;
    const amount = document.getElementById("amount").value;

    fetch("/withdraw", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, address, amount })
    }).then(res => res.json())
      .then(() => alert("So‘rov yuborildi, admin tasdiqlashini kuting ✅"));
});
