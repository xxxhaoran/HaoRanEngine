// 输入的密码框
let input = document.getElementById('input')
let input1 = document.getElementById('input1')
let input2 = document.getElementById('input2')
let eyes = document.getElementById('eyes')
let eyes1 = document.getElementById('eyes1')
let eyes2 = document.getElementById('eyes2')
let ReBtn = document.getElementById('submitBtn1')
let LoBtn = document.getElementById('submitBtn2')


var flag = false;

eyes.onclick = function () {
    flag = !flag
    if (flag) {
        input.type = 'text';
        eyes.className = 'fa fa-eye fa1'
    } else{
        input.type = 'password';
        eyes.className = 'fa fa-eye-slash fa1'
    }
}
eyes1.onclick = function () {
    console.log("eye1");
    flag = !flag
    if (flag) {
        input1.type = 'text';
        eyes1.className = 'fa fa-eye fa2'
    } else{
        input1.type = 'password';
        eyes1.className = 'fa fa-eye-slash fa2'
    }
}
eyes2.onclick = function () {
    console.log("eye2");
    flag = !flag
    if (flag) {
        input2.type = 'text';
        eyes2.className = 'fa fa-eye fa3'
    } else{
        input2.type = 'password';
        eyes2.className = 'fa fa-eye-slash fa3'
    }
}
// 获取要操作的元素
let login_title = document.querySelector('.login-title');
let register_title = document.querySelector('.register-title');
let login_box = document.querySelector('.login-box');
let register_box = document.querySelector('.register-box');

// 绑定标题点击事件
login_title.addEventListener('click', () => {
    // 判断是否收起，收起才可以点击
    if (login_box.classList.contains('slide-up')) {
        register_box.classList.add('slide-up');
        login_box.classList.remove('slide-up');
    }
})
register_title.addEventListener('click', () => {
    if (register_box.classList.contains('slide-up')) {
        login_box.classList.add('slide-up');
        register_box.classList.remove('slide-up');
    }
})

document.addEventListener('keydown', function(event) {
    if (document.activeElement === input || document.activeElement === input1) {
        if (event.key === 'Enter') {
            ReBtn.onclick()
        }
        ;
    }
    else if (document.activeElement === input2)
    {
        if (event.key === 'Enter') {
            LoBtn.onclick()
        }
        ;
    }
});

// 提交按钮点击事件处理函数
ReBtn.onclick = function () {
    let userValue = document.getElementById('user0').value;
    let inputValue = input.value;
    let input1Value = input1.value;
    if (inputValue!=input1Value){
        alert('密码不一致!')
        return 0
    }
    // 构造要提交的数据对象
    let data = {
        user: userValue,
        input: inputValue,
        input1: input1Value
    };

    // 发送POST请求到服务器
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // 处理服务器返回结果
        alert(result['message'])
        console.log(result);
    })
    .catch(error => {
        // 处理错误
        console.error(error);
    });
};

// 提交按钮点击事件处理函数
LoBtn.onclick = function () {
    let userValue = document.getElementById('user1').value;
    let passwordValue = input2.value;
    if (passwordValue.length<6){
        alert('密码长度小于6位!')
        return 0
    }
    // 构造要提交的数据对象
    let data = {
        user: userValue,
        pass: passwordValue,
    };

    // 发送POST请求到服务器
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // 处理服务器返回结果
        alert(result['message'])
        if(result['message']=='登录成功!') window.location.replace ("/")
        console.log(result);
    })
    .catch(error => {
        // 处理错误
        console.error(error);
    });
};


