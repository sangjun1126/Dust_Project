const commentBtn = document.querySelector("#commentFrm");
const commentList = document.querySelector("#comment-list");
const total = document.querySelector("h4 > span");
const list = [];

function Comment(content) {
    this.userid = 'sangjun';
    this.content = content;
    this.date = "2023-12-01";
}

function createRow(userid, content, date) {
    const ul = document.createElement('ul');
    const li1 = document.createElement('li');
    const li2 = document.createElement('li');
    const li3 = document.createElement('li');
    
    ul.append(li1);
    ul.append(li2);
    ul.append(li3);

    ul.setAttribute('class', 'comment-row');
    li1.setAttribute('class', 'comment-id');
    li2.setAttribute('class', 'comment-content');
    li3.setAttribute('class', 'comment-date');

    li1.innerHTML = userid;
    li2.innerHTML = content;
    li3.innerHTML = date;

    return ul;
}

function drawing() {
    commentList.innerHTML = "";
    for (let i = list.length - 1; i >= 0; i-= 1) {
        const row = createRow(list[i].userid, list[i].content, list[i].date);
        commentList.append(row);
    }
}

function totlaRecord() {
    total.innerHTML = `(${list.length})`;
}

function commentBtnHandler(e) {
    e.preventDefault();
    const input = e.target.content;
    if (input.value === "") {
        alert('내용을 넣고 등록 버튼을 눌러주세요');
        return;
    }
    const commentObj = new Comment(input.value);
    list.push(commentObj);
    totlaRecord();

    drawing();
    e.target.reset();
}

totlaRecord();
commentBtn.addEventListener("submit",commentBtnHandler);