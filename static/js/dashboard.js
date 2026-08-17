// ================================
// Dashboard Charts
// ================================

let tasksChart = null;
let assignmentsChart = null;


// ================================
// Get Chart Text Color
// ================================

function getChartTextColor() {

    return document.body.classList.contains("dark-mode")
        ? "#f9fafb"
        : "#374151";
}


// ================================
// Update Charts Colors
// ================================

function updateChartsColors() {

    const textColor = getChartTextColor();

    if (tasksChart) {

        tasksChart.options.plugins.legend.labels.color =
            textColor;

        tasksChart.update();
    }

    if (assignmentsChart) {

        assignmentsChart.options.plugins.legend.labels.color =
            textColor;

        assignmentsChart.update();
    }
}


// ================================
// Create Charts
// ================================

document.addEventListener("DOMContentLoaded", function () {


    // ================================
    // Tasks Chart
    // ================================

    const tasksCanvas =
        document.getElementById("tasksChart");


    if (tasksCanvas) {

        const completed =
            Number(
                tasksCanvas.dataset.completed || 0
            );

        const pending =
            Number(
                tasksCanvas.dataset.pending || 0
            );


        tasksChart = new Chart(
            tasksCanvas,
            {

                type: "doughnut",


                data: {

                    labels: [
                        "Completed",
                        "Pending"
                    ],


                    datasets: [
                        {

                            data: [
                                completed,
                                pending
                            ],


                            backgroundColor: [
                                "#6366f1",
                                "#cbd5e1"
                            ],


                            borderWidth: 0
                        }
                    ]
                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,


                    plugins: {

                        legend: {

                            display: true,

                            position: "bottom",


                            labels: {

                                color:
                                    getChartTextColor(),

                                padding: 20,

                                usePointStyle: true,


                                font: {
                                    size: 14
                                },


                                generateLabels:
                                    function (chart) {

                                        const data =
                                            chart.data;


                                        return data.labels.map(
                                            function (
                                                label,
                                                index
                                            ) {

                                                const value =
                                                    data.datasets[0]
                                                        .data[index];


                                                return {

                                                    text:
                                                        label +
                                                        " (" +
                                                        value +
                                                        ")",


                                                    fillStyle:
                                                        data.datasets[0]
                                                            .backgroundColor[index],


                                                    strokeStyle:
                                                        data.datasets[0]
                                                            .backgroundColor[index],


                                                    fontColor:
                                                        getChartTextColor(),


                                                    hidden: false,


                                                    index: index
                                                };

                                            }
                                        );
                                    }
                            }
                        },


                        tooltip: {

                            callbacks: {

                                label:
                                    function (context) {

                                        return (
                                            context.label +
                                            ": " +
                                            context.raw +
                                            " tasks"
                                        );

                                    }
                            }
                        }
                    }
                }
            }
        );
    }


    // ================================
    // Assignments Chart
    // ================================

    const assignmentsCanvas =
        document.getElementById(
            "assignmentsChart"
        );


    if (assignmentsCanvas) {

        const completedAssignments =
            Number(
                assignmentsCanvas.dataset.completed || 0
            );


        const pendingAssignments =
            Number(
                assignmentsCanvas.dataset.pending || 0
            );


        const inProgressAssignments =
            Number(
                assignmentsCanvas.dataset.inProgress || 0
            );


        assignmentsChart = new Chart(
            assignmentsCanvas,
            {

                type: "doughnut",


                data: {

                    labels: [
                        "Completed",
                        "Pending",
                        "In Progress"
                    ],


                    datasets: [
                        {

                            data: [
                                completedAssignments,
                                pendingAssignments,
                                inProgressAssignments
                            ],


                            backgroundColor: [
                                "#6366f1",
                                "#cbd5e1",
                                "#a5b4fc"
                            ],


                            borderWidth: 0
                        }
                    ]
                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,


                    plugins: {

                        legend: {

                            display: true,

                            position: "bottom",


                            labels: {

                                color:
                                    getChartTextColor(),

                                padding: 15,

                                usePointStyle: true,


                                font: {
                                    size: 14
                                },


                                generateLabels:
                                    function (chart) {

                                        const data =
                                            chart.data;


                                        return data.labels.map(
                                            function (
                                                label,
                                                index
                                            ) {

                                                const value =
                                                    data.datasets[0]
                                                        .data[index];


                                                return {

                                                    text:
                                                        label +
                                                        " (" +
                                                        value +
                                                        ")",


                                                    fillStyle:
                                                        data.datasets[0]
                                                            .backgroundColor[index],


                                                    strokeStyle:
                                                        data.datasets[0]
                                                            .backgroundColor[index],


                                                    fontColor:
                                                        getChartTextColor(),


                                                    hidden: false,


                                                    index: index
                                                };

                                            }
                                        );
                                    }
                            }
                        },


                        tooltip: {

                            callbacks: {

                                label:
                                    function (context) {

                                        return (
                                            context.label +
                                            ": " +
                                            context.raw +
                                            " assignments"
                                        );

                                    }
                            }
                        }
                    }
                }
            }
        );
    }

});