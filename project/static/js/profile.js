$(document).ready(function(){

    var edit_id = 0; //used in dialog


    // -----Copy Password-----//

    $(".b_copy").click(function(){
        
        var copy_id = $(this).closest('tr').attr('id');
        var action = "copy";
        var dataObj = {"id": copy_id, "action": action};
        
        $.ajax({
            type:'POST',
            url: '/profile/copy',
            contentType: "application/json",
            data: JSON.stringify(dataObj),
            //dataType:"json", //this is the return type
            success: function(result){
                // copy to clipboard
                let copyFrom = document.createElement("textarea");
                document.body.appendChild(copyFrom);
                copyFrom.textContent = result;
                copyFrom.select();
                document.execCommand("copy");
                copyFrom.remove();
            }
        })
    });

    // ------ Edit ------//

    // -----Edit Password -----//

    $("#dialog_pw").dialog({
        autoOpen: false,
        buttons: { 
            Ok: function() {
                var key = $("#edit_pw").val()
                var action = "edit_key";
                // var edit_id = $("#dialog").data(edit_id);
                var dataObj = {"id": edit_id, "action": action, "key": key};
                console.log(edit_id);
                console.log(dataObj);
                $.ajax({
                    type:'POST',
                    url: '/profile/edit_key',
                    contentType: "application/json",
                    data: JSON.stringify(dataObj),
                    success: function(result){
                        alert(result);
                        window.location.reload();
                    }
                })
                $(this).dialog("close");
                $("#dialog_pw").hide();
           },
            Cancel: function () {
                $(this).dialog("close");
                $("#dialog_pw").hide();
            }
        },
        close: function() {
             $("#edit_pw").val(''); 
             $("#dialog_pw").hide();
            }
    });


    $(".b_edit").on({
            click: function() {
            
            $("#dialog_pw").show();
            edit_id = $(this).closest('tr').attr('id');
            $("#dialog_pw").dialog("open");

        }, touch: function() {
            // mobile
            $("#dialog_pw").show();
            $(".b_edit").draggable();
            edit_id = $(this).closest('tr').attr('id');
            $("#dialog_pw").dialog("open");

        }
      });


    // -----Edit Username ------//

    $("#dialog_key_name").dialog({
        autoOpen: false,
        buttons: { 
            Ok: function() {
                var key_name = $("#edit_key_name").val()
                var action = "edit_key_name";
                var dataObj = {"id": edit_id, "action": action, "key_name": key_name};
                console.log(edit_id);
                console.log(dataObj);
                $.ajax({
                    type:'POST',
                    url: '/profile/edit_key_name',
                    contentType: "application/json",
                    data: JSON.stringify(dataObj),
                    success: function(result){
                        alert(result);
                        window.location.reload();
                    }
                })
                $(this).dialog("close");
                $("#dialog_key_name").hide();
           },
            Cancel: function () {
                $(this).dialog("close");
                $("#dialog_key_name").hide();
            }
        },
        close: function() { 
                $("#edit_key_name").val(''); 
                $("#dialog_key_name").hide();    
            }
    });


    $(".td_edit").dblclick(function(){
        $("#dialog_key_name").show();
        edit_id = $(this).closest('tr').attr('id');
        $("#dialog_key_name").dialog("open");
    });


    $(".td_edit").on("taphold", function(){
        $("#dialog_key_name").show();
        $(".td_edit").draggable();
        edit_id = $(this).closest('tr').attr('id');
        $("#dialog_key_name").dialog("open");
    });


    // ----- Edit Description ----- //
    $("#dialog_desc").dialog({
        autoOpen: false,
        buttons: { 
            Ok: function() {
                var key_desc = $("#edit_desc").val()
                var action = "edit_key_description";
                var dataObj = {"id": edit_id, "action": action, "key_desc": key_desc};
                console.log(edit_id);
                console.log(dataObj);
                $.ajax({
                    type:'POST',
                    url: '/profile/edit_key_description',
                    contentType: "application/json",
                    data: JSON.stringify(dataObj),
                    success: function(result){
                        alert(result);
                        window.location.reload();
                    }
                })
                $(this).dialog("close");
                $("#dialog_desc").hide();
           },
            Cancel: function () {
                $(this).dialog("close");
                $("#dialog_desc").hide();
            }
        },
        close: function() { 
                $("#edit_desc").val(''); 
                $("#dialog_desc").hide();    
            }
    });


    $(".td_desc").dblclick(function(){
        $("#dialog_desc").show();
        edit_id = $(this).closest('tr').attr('id');
        $("#dialog_desc").dialog("open");
    });

    $(".td_desc").on("taphold", function(){
        $("#dialog_desc").show();
        $(".td_desc").draggable();
        edit_id = $(this).closest('tr').attr('id');
        $("#dialog_desc").dialog("open");
    });

    // ----- Delete -----//

    $(".b_delete").click(function(){
        
        var r = confirm("Are you sure to delete?");
        if (r == true) {
            var delete_id = $(this).closest('tr').attr('id');
            var action = "delete";
            var dataObj = {"id": delete_id, "action": action};
            
            $.ajax({
                type:'POST',
                url: '/profile/delete',
                contentType: "application/json",
                data: JSON.stringify(dataObj),
                success: function(result){
                    alert(result);
                    window.location.reload();
                }
            })
        } else {
            console.log("cancel delete");
        }

    });


});