document.getElementById("startCapture").addEventListener("click", function () {
    let numPages = document.getElementById("numPages").value;
    let pdfName = document.getElementById("pdfName").value.trim();

    if (!numPages || numPages <= 0) {
        alert("Please enter a valid number of pages!");
        return;
    }
    if (!pdfName) {
        alert("Please enter a name for the PDF!");
        return;
    }

    document.getElementById("status").innerText = "Starting in 5 seconds... Switch to the tab!";
    
    setTimeout(() => {
        document.getElementById("status").innerText = "Capturing screenshots...";

        fetch(`/capture?pages=${numPages}&name=${pdfName}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById("status").innerText = "Screenshots captured successfully!";
                document.getElementById("downloadSection").style.display = "block";

                document.getElementById("downloadPDF").setAttribute("data-name", pdfName);
                document.getElementById("downloadWord").setAttribute("data-name", pdfName);
            })
            .catch(error => {
                document.getElementById("status").innerText = "Error capturing screenshots.";
                console.error("Error:", error);
            });

    }, 5000); // 5 seconds delay
});

document.getElementById("downloadPDF").addEventListener("click", function () {
    let pdfName = this.getAttribute("data-name");
    window.location.href = `/download/pdf?name=${pdfName}`;
});

document.getElementById("downloadWord").addEventListener("click", function () {
    let pdfName = this.getAttribute("data-name");
    window.location.href = `/download/word?name=${pdfName}`;
});
