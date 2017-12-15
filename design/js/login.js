function sujixy(max, min) {
    return parseInt(Math.random() * (max - min + 1) + min);
}

function Xq() {
    //随机定位
    this.left = sujixy(document.body.clientWidth - 20, 0); 
    this.top = sujixy(10, 0);
    this.dx = sujixy(20, 10);
}
Xq.prototype = {
    //产生一个随机位置，随机颜色随机大小的小球。
    xq: function() {
        this.ba = document.createElement("img");
        this.ba.src ="../img/white-snowflake.png";
        this.ba.style.width = this.dx + "px";
        this.ba.style.height = this.dx + "px";
        this.ba.style.position = "absolute";
        this.ba.style.left = this.left + "px";
        this.ba.style.top = this.top + "px";
        document.body.appendChild(this.ba);
    },
    //产生一个小球移动碰撞的方法。
    xqd: function() {
        var l = 0;
        var t = 1;
        var left1 = this.left;
        var top1 = this.top;
        var _this = this;
        var ID = setInterval(function() {
            left1 += l;
            top1 += t;
            _this.ba.style.left = left1 + "px";
            _this.ba.style.top = top1 + "px";
            if (top1 >= innerHeight - _this.dx) {
                document.body.removeChild(_this.ba);
                clearInterval(ID);
            }
        }, 10);
    }
}
set = setInterval(fun, 300);

function fun() {
    var a = new Xq();
    a.xq();
    a.xqd();
}