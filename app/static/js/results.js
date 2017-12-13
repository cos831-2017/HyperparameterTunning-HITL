var mockdata = {
  'experiment_id': 42,
  'block_data': [{
    'block_id': 3,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98]
  }, {
    'block_id': 0,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.766, 0.65]
  }]
};

// Shorthand for $( document ).ready()
$(function() {
  // Chart.js scripts
  // -- Set new default font family and font color to mimic Bootstrap's default styling
  Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
  Chart.defaults.global.defaultFontColor = '#292b2c';

  (function worker() {
    $.ajax({
      url: '/blockresults',
      success: function(data) {
        // if (isNone(data)) {
        //   data = mockdata;
        // }
        processBlocksData(data);
      },
      complete: function() {
        // Schedule the next request when the current one's complete
        setTimeout(worker, 5000);
      },
      error: function() {
        alert("erro!");
      }
    });
  })();

});

var blocks = {};

function processBlocksData(data) {
  if (isNone(data)) {
    return;
  }

  var blocksData = data['block_data'];

  if (isNone(blocksData)) {
    return;
  }

  // alert(JSON.stringify(blocksData));

  for (let blockData of blocksData) {
    if (!(blockData['block_id'] in blocks)) {
      blocks[blockData['block_id']] = blockData;
      addNewBlock(blockData);
    }
  }
}

function makeLabels(data) {
  var labelIds = data['labels'].map(function(valorAtual, indice, array) {
    return 'C' + indice;
  });

  return labelIds;
}

function addNewBlock(data) {
  if (typeof data === 'undefined' || !data || jQuery.isEmptyObject(data)) {
    return;
  }

  var newBlockDiv = $("#block-card-").clone();
  $(newBlockDiv).prop("id", "block-card-" + data['block_id']);
  $(newBlockDiv).find("#block-header").append(data['block_id']);
  $("#blocks").append(newBlockDiv);
  $(newBlockDiv).show();

  var divDetails = $(newBlockDiv).find("#block-details");

  // get bar chart canvas
  var mychart = $(newBlockDiv).find("#block-chart")[0].getContext("2d");

  var labelIds = makeLabels(data);

  var barData = arangeAccuracyData(labelIds, data);

  for (var i = 0; i < labelIds.length; i++) {
    $('<li />', {
      html: labelIds[i] + ' - ' + data['labels'][i]
    }).appendTo($(divDetails).find('ul.combination-list'));
  }

  steps = 1
  max = 1
  // draw bar chart
  var blockBarChart = new Chart(mychart, {
    type: 'bar',
    data: barData,
    options: {
      // responsive: false,
      scaleOverride: true,
      scaleSteps: steps,
      scaleStepWidth: Math.ceil(max / steps),
      scaleStartValue: 0,
      scaleShowVerticalLines: true,
      scaleShowGridLines: true,
      barShowStroke: true,
      scaleShowLabels: true,
      scales: {
        yAxes: [{
          ticks: {
            min: 0,
            max: 1,
          },
          gridLines: {
            display: true
          }
        }],
      },
      legend: {
        display: true
      }
    }
  });
}

function arangeAccuracyData(labels, data) {
  var values = data['accuracy'];

  // bar chart data
  var barData = {
    labels: labels,
    datasets: [{
      label: "Accuracy",
      backgroundColor: "rgba(2,117,216,1)",
      borderColor: "rgba(2,117,216,1)",
      fillColor: "rgba(151,187,205,0.2)",
      strokeColor: "rgba(151,187,205,1)",
      pointColor: "rgba(151,187,205,1)",
      data: values
    }]
  }

  return barData;
}

/*
// -- Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["Mar 1", "Mar 2", "Mar 3", "Mar 4", "Mar 5", "Mar 6", "Mar 7", "Mar 8", "Mar 9", "Mar 10", "Mar 11", "Mar 12", "Mar 13"],
    datasets: [{
      label: "Sessions",
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 20,
      pointBorderWidth: 2,
      data: [10000, 30162, 26263, 18394, 18287, 28682, 31274, 33259, 25849, 24159, 32651, 31984, 38451],
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 40000,
          maxTicksLimit: 5
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
// -- Bar Chart Example
var ctx = document.getElementById("myBarChart");
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ["January", "February", "March", "April", "May", "June"],
    datasets: [{
      label: "Revenue",
      backgroundColor: "rgba(2,117,216,1)",
      borderColor: "rgba(2,117,216,1)",
      data: [4215, 5312, 6251, 7841, 9821, 14984],
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'month'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 6
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 15000,
          maxTicksLimit: 5
        },
        gridLines: {
          display: true
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
// -- Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ["Blue", "Red", "Yellow", "Green"],
    datasets: [{
      data: [12.21, 15.58, 11.25, 8.32],
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
    }],
  },
});
*/