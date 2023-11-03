const conf = {
    maxRemote: 1,
    maxItem: [],
    remotes: {}
}

const item = {
    remote: 0,
    member: 1,
    group: 1,
}


async function getConfig() {
    const url = "/api/config";
    const response = await fetch(url);
    let tmp = await response.json();
    conf.remotes = tmp.remotes

    conf.maxRemote = conf.remotes.length

    for (let remote of conf.remotes) {
        let maxGroup = remote.length;
        let maxRemote = {'maxGroup': maxGroup, 'group': []};

        for (let group of remote) {
            maxRemote.group.push(group.members.length);
        }
        conf.maxItem.push(maxRemote);
    }

    document.getElementById("member-num").innerHTML = item.member;
    document.getElementById("group-num").innerHTML = item.group;
    document.getElementById("member").innerHTML = conf.remotes[item.remote][item.group].members[item.member];
    document.getElementById("group").innerHTML = conf.remotes[item.remote][item.group].name;
}

function updateDisplay(type, factor) {
    let maxGroup = conf.maxItem[item.remote].maxGroup;
    let maxMember = conf.maxItem[item.remote].group[item.group];

    if (type === "remote") {
        item.remote += factor;

        if (item.remote >= conf.maxRemote) {
            item.remote = 0;
        } else if (item.remote < 0) {
            item.remote = conf.maxRemote-1;
        }

        // Overflow check
        maxGroup = conf.maxItem[item.remote].maxGroup;
        if (item.group >= maxGroup) {
            item.group = maxGroup-1;
        }
        maxMember = conf.maxItem[item.remote].group[item.group];
        if (item.member >= maxMember) {
            item.member = maxMember-1;
        }

    } else if (type === "member") {
        item.member += factor

        if (item.member >= maxMember) {
            item.member = 0;
        } else if (item.member < 0) {
            item.member = maxMember-1;
        }
    } else if (type === "group") {
        item.group += factor;

        if (item.group >= maxGroup) {
            item.group = 0;
        } else if (item.group < 0) {
            item.group = maxGroup-1;
        }

        // Overflow check
        maxMember = conf.maxItem[item.remote].group[item.group];
        if (item.member >= maxMember) {
            item.member = maxMember-1;
        }
    }
    document.getElementById("member-num").innerHTML = item.member;
    document.getElementById("group-num").innerHTML = item.group;
    document.getElementById("member").innerHTML = conf.remotes[item.remote][item.group].members[item.member];
    document.getElementById("group").innerHTML = conf.remotes[item.remote][item.group].name;
}

async function postData(cmd) {
    let data = {
        "remote": item.remote,
        "member": item.member,
        "group": item.group,
        "cmd": cmd
    }

    console.log("Sending command:", data)
    const response = await fetch('/api/cmd', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    });

}