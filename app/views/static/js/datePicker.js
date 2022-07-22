$(function() {
    let start = moment();
    let end = moment().add(1,'day');

    function cb(start, end) {
        $('#reportrange span').html(start.format('DD-MM-YYYY') + ' - ' + end.format('DD-MM-YYYY'));
    }

    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        minDate: start
    }, cb);

    cb(start, end);

});