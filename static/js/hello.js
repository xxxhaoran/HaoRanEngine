function time() {
    var timer = new Date();
    var hour = timer.getHours();
    var min = timer.getMinutes();
    if (hour < 10) {
        hour = "0" + hour + ":";
    } else {
        hour = hour + ":";
    }
    if (min < 10) {
        min = "0" + min + "";
    } else {
        min = min + "";
    }
    document.querySelector(".time").innerHTML = hour + '' + min;
    setTimeout(time, 1000);
}
function helloFloat(username='尊敬的用户') {
    // 获得元素
    var hello = document.getElementById('hello')
    var image = document.getElementById('image')
    // 获得时间对象
    var gettime = new Date();
    var hours = gettime.getHours();
    var str1 = "Good morning!"+username
    var str2 = "Good afternoon!"+username
    var str3 = "Good night!"+username
    // 判断
    if (hours > 6 && hours <= 11) {
        hello.innerHTML = str1;
        image.src = "../static/images/day.jpeg"
        switchBtn.className = 'fa fa-sun-o'
    } else if (hours > 11 && hours <= 20) {
        hello.innerHTML = str2
        if (hours >= 17) {
            image.src = "../static/images/afternoon.jpeg"
        } else {
            image.src = "../static/images/day.jpeg"
        }
        switchBtn.className = 'fa fa-sun-o'
    } else {
        hello.innerHTML = str3
        image.src = "../static/images/night.jpeg"
        switchBtn.className = 'fa fa-moon-o'
        switchBtn.style.color = 'rgba(32,33,36,.25)'
    }
}
// 输入框
let search = document.getElementById('search')
let bg = document.getElementById('bg')
let value = document.getElementById('search').value
let poem = document.getElementById('poem')
value = "Search"
search.onfocus = function () {
    search.value = ''
    // 背景高斯模糊
    bg.style.WebkitFilter = "blur(6px)";
    // 背景放大
    bg.style.transform = "scale(1.05)";
    // 修改诗歌的类名
    poem.className = 'poem';
    // 搜索框变长

}
search.onblur = function () {
    search.value = 'Search'
    bg.style.WebkitFilter = "blur(0px)";
    bg.style.transform = "scale(1)";
    poem.className = 'hide';
}

$('input').on("keydown",function(event){
    var keyCode = event.keyCode || event.which;
    if(keyCode == "13"){
        open('https://www.baidu.com/s?wd='+document.getElementById('search').value);
    }
});

//输入框 结束
