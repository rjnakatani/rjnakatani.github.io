var options = {
    series: [],
    chart: {
        height: 350,
        type: 'bar',
    },
    plotOptions: {
        bar: {
            borderRadius: 10,
            dataLabels: {
                position: 'top', // top, center, bottom
            },
        }
    },
    dataLabels: {
        enabled: false,
    },
    noData: {
        text: 'No Data'
    },

    xaxis: {
        type: 'category',
          tickPlacement: 'on',
          labels: {
            rotate: -45,
            rotateAlways: true        
          },
        axisTicks: {
            show: false
        },
        crosshairs: {
            fill: {
                type: 'gradient',
                gradient: {
                    colorFrom: '#D8E3F0',
                    colorTo: '#BED1E6',
                    stops: [0, 100],
                    opacityFrom: 0.4,
                    opacityTo: 0.5,
                }
            }
        },
        tooltip: {
            enabled: true,
        }
    },
    yaxis: {
        axisBorder: {
            show: false
        },
        axisTicks: {
            show: false,
        },
        labels: {
            show: false,
            formatter: function (val) {
                return val + " count";
            }
        },    
    },
    title: {
        text: 'Research Activities',
        floating: true,
        offsetY: 300,
        align: 'center',
        style: {
            color: '#444'
        },
    },    
};

var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();

$.getJSON('/assets/charts/first_author.json', function(response) {
    chart.updateSeries([{
        name: 'First Author',
        data: response
    }])
});
$.getJSON('/assets/charts/presentation.json', function(response) {
    chart.appendSeries({
        name: 'Presentations',
        data: response
    })
});
// chart.updateOptions({
//     legend: {
//         position: 'right'
//     }
// });
// chart.render();
