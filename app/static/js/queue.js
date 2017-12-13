// Shorthand for $( document ).ready()
$(function() {
  renderTable();
});

var tableQueue;

function renderTable(data) {
  tableQueue = $('#block-table').DataTable({
    ajax: "blockqueue",
    "columnDefs": [{
      "targets": -1,
      "data": null,
      "render": function(data, type, row) {
        return row[4] == ' Waiting ' ?
        "<button class='btn btn-outline-primary move-up steer'>Move Up</button> \
        <button class='btn btn-outline-primary move-down steer'>Move Down</button> \
        <button class='btn btn-outline-primary remove steer'>Remove</button>"
        : ' - ';
      },
    }, {
      'bSortable': false,
      'aTargets': [1, 2, 3, 4, 5]
    }, ]
  });

  updateTableEvents();
  setReloadOfTable();
}

function setReloadOfTable(){
  setInterval( function () {
    tableQueue.ajax.reload( null, false ); // user paging is not reset on reload
    updateTableEvents();
  }, 1500 );
}

function remove(block_id){
  $('#block-table tbody button.steer').attr("disabled", true);
  $.ajax({
    url: '/removeblock/' + block_id,
    method: "GET",
    success: function(data) {
      console.log('sucesso')
    },
    complete: function() {
      $('#block-table tbody button.steer').removeAttr("disabled");
    },
    error: function() {
      alert("erro!");
    }
  });
}

function moveUp(block_id){
  $('#block-table tbody button.steer').attr("disabled", true);
  $.ajax({
    url: '/moveup/' + block_id,
    method: "GET",
    success: function(data) {
      console.log('sucesso')
    },
    complete: function() {
      $('#block-table tbody button.steer').removeAttr("disabled");
    },
    error: function() {
      alert("erro!");
    }
  });
}

function moveDown(block_id){
  $('#block-table tbody button.steer').attr("disabled", true);
  $.ajax({
    url: '/movedown/' + block_id,
    method: "GET",
    success: function(data) {
      console.log('sucesso')
    },
    complete: function() {
      $('#block-table tbody button.steer').removeAttr("disabled");
    },
    error: function() {
      alert("erro!");
    }
  });
}

function updateTableEvents() {
  $('#block-table tbody').off('click', 'button.move-up');
  $('#block-table tbody').off('click', 'button.move-down');
  $('#block-table tbody').off('click', 'button.remove');

  $('#block-table tbody').on('click', 'button.move-up', function() {
    var data = tableQueue.row($(this).parents('tr')).data();
    moveUp(data[1]);
  });

  $('#block-table tbody').on('click', 'button.move-down', function() {
    var data = tableQueue.row($(this).parents('tr')).data();
    moveDown(data[1]);
  });

  $('#block-table tbody').on('click', 'button.remove', function() {
    var data = tableQueue.row($(this).parents('tr')).data();
    remove(data[1]);
  });
}
