$(function() {
    const firstDateInput = document.getElementById("dateInit");
    const secondDateInput = document.getElementById("dateFinal");
    let start = moment();
    let end = moment().add(1,'day');

    function cb(start, end) {
        $('#initialDatePicked').html(start.format('YYYY-MM-DD'));
        $('#finalDatePicked').html(end.format('YYYY-MM-DD'));

        firstDateInput.value=start.format('YYYY-MM-DD');
        secondDateInput.value=end.format('YYYY-MM-DD');
    }

    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        minDate: start,
        autoApply: true
    }, cb);

    cb(start, end);

});