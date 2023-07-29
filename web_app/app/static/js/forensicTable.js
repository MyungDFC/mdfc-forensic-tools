function checkAll() {
    let checkboxes = document.querySelector('#flexCheckAll');
    let checkboxesChecked = document.querySelector('#flexCheckRow');
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxesChecked.checked) {
            checkboxes[i].checked = true;
        } else {
            checkboxes[i].checked = false;
        }
    }
}

