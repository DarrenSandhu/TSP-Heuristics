function runBenchmark() {
    var algorithm = document.getElementById("algorithm").value;

    if (algorithm === "--") {
        alert("Please select an algorithm.");
        return;
    }

    // Additional checks for specific algorithm options
    if (algorithm === "mtz") {
        var timeLimit = document.getElementById("time-limit").value;
        var mipGap = document.getElementById("mip-gap").value;
        var printLog = document.getElementById("print-log").value;

        // Validate input values (e.g., check if they are valid numbers)
        // Run the benchmark with the provided options
        // Example: call a function to perform the benchmarking process
        performBenchmark(algorithm, timeLimit, mipGap, printLog);
    } else {
        // Run the benchmark with the selected algorithm (without additional options)
        // Example: call a function to perform the benchmarking process
        performBenchmark(algorithm);
    }
}

function performBenchmark(algorithm, timeLimit, mipGap, printLog) {
    // Send a request to the server to run the benchmark with the provided options
    // Example: use AJAX to call a backend script that executes the benchmarking code
    // Once the benchmarking is complete, display the graph
    document.getElementById("graph-image").src = "benchmark_graph.png";
    document.querySelector(".graph-content").style.display = "block";
}