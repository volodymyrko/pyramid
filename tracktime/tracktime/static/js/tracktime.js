function generateTime()
    {
        var second = time % 60;
        var minute = Math.floor(time / 60) % 60;
        var hour = Math.floor(time / 3600) % 60;

        second = (second < 10) ? '0'+second : second;
        minute = (minute < 10) ? '0'+minute : minute;
        hour = (hour < 10) ? '0'+hour : hour;

        $('div.timer span.second').html(second);
        $('div.timer span.minute').html(minute);
        $('div.timer span.hour').html(hour);
    }

function _timer(){
    var st = 0;

    this.reset =  function(sec){
        sec = (typeof(sec) !== 'undefined') ? sec : 0;
        time = sec;
        generateTime(time);
    }

    this.start = function(interval){
            interval = 1000;
            if(st == 0) {
                st = 1;
                timer_id = setInterval(function()
                {
                        if(time < 86400)
                        {
                            time++;
                            generateTime();
                            //if(typeof(callback) === 'function') callback(time);
                        }
                }, interval);
            }
    }

    this.stop =  function(){
        if(st == 1)
        {
            st = 0;
            clearInterval(timer_id);
        }
    };
}

$(document).ready(function(){
    timer = new _timer();
    
    function initialize_timer(){
        $.ajax({
            url: '/counter/status/',
            dataType: 'json',
            success: function(data, textStatus, jqXHR){
                console.log(data);
                if(data['status'] === 'new'){
                    console.log('new');
                    timer.reset(0);
                    $('#start_btn').fadeIn('slow');
                }
                else if(data['status'] === 'continue'){
                    console.log('continue');
                    id = data['id'];
                    timer.reset(data['sec']);
                    timer.start()
                    $('#stop_btn').fadeIn('slow');
                }
            },
        });
    }

    function start_tracktime(){
        $.ajax({
            url: '/counter/start/',
            dataType: 'json',
            success: function(data, textStatus, jqXHR){
                if(data['status'] === 1){
                    console.log(data['id']);
                    id = data['id']
                }
                else if(data['status'] === 0){
                    alert('Error, Retry please');
                    timer.stop();
                    timer.reset(0);
                }
            },
            error: function(){
                timer.stop();
                timer.reset(0);
                alert('Error, Retry please');
            },
        })
    }
    function stop_tracktime(){
        $.ajax({
            url: '/counter/stop/' + id + '/',
            dataType: 'json',
            success: function(data, textStatus, jqXHR){
                if(data['status'] === 0){
                    alert('Error, Retry please');
                }
            },
            error: function(){
                    alert('Error, Retry please');
            },
        })
    }

    function msg_save(){
        $.ajax({
            url: '/counter/msg/' + id + '/',
            dataType: 'json',
            type: 'POST',
            data: 'data=' + $('#msg_text').val(),
            success: function(data, textStatus, jqXHR){
                if(data['status'] === 0){
                    alert('Error, Retry please');
                }
                else if(data['status'] === 1){
                    $('#msg_text').val('');
                    timer.reset(0);
                    $('#stop_btn').fadeOut('slow');
                    $('#track_msg').fadeOut('slow');
                    $('#start_btn').fadeIn('slow');
                }

            },
            error: function(){
                    alert('Error, Retry please');
            },
        })
    }


    initialize_timer();

    $("#start_btn").click(function(){
        timer.reset(0);
        timer.start()
        $('#start_btn').fadeOut('slow');
        $('#stop_btn').fadeIn('slow');
        start_tracktime();
        return false;
    })
    $("#stop_btn").click(function(){
        timer.stop()
        $('#track_msg').fadeIn('slow');
        stop_tracktime();
        return false;
    });
    $('#msg_btn_save').click(function(){
        msg_save();
        return false;
    })



});
