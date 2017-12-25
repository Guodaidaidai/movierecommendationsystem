function collection(m_id,u_id){
    var gnl=confirm(u_id);
    if (gnl==false){
        return;
    }
     $.ajax({

    url: "/comment/user/collect/add/",
    data: {'m_id': m_id,'u_id':u_id},
    type: 'POST',

    success: function(data){
        if (data.errcode == "1"){
            alert("OK");
            window.location.reload();
        }
        else{
            alert("errmsg: " + data.errmsg)
        }
    }
})
}
