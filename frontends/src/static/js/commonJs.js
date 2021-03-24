export function handleAllUser(usersjson){
    var handledUsers = [];
    var groupName1 = "业务一课";
    var groupName2 = "业务二课";
    var groupName3 = "业务三课";
    var groupName4 = "制品一课";
    var group1 = { label: groupName1, options: [] };
    var group2 = { label: groupName2, options: [] };
    var group3 = { label: groupName3, options: [] };
    var group4 = { label: groupName4, options: [] };
    for (var i in usersjson) {
        var option = {};
        if (usersjson[i]["ammic_group"]){
            if (usersjson[i]["ammic_group"]["name"] == groupName1) {
            option = { value: usersjson[i]["name"], label: usersjson[i]["name"] };
            group1["options"].push(option);
            }

            if (usersjson[i]["ammic_group"]["name"] == groupName2) {
            option = { value: usersjson[i]["name"], label: usersjson[i]["name"] };
            group2["options"].push(option);
            }

            if (usersjson[i]["ammic_group"]["name"] == groupName3) {
            option = {
                value: usersjson[i]["name"],
                label: usersjson[i]["name"],
            };
            group3["options"].push(option);
            }

            if (usersjson[i]["ammic_group"]["name"] == groupName4) {
            option = {
                value: usersjson[i]["name"],
                label: usersjson[i]["name"],
            };
            group4["options"].push(option);
            }
        }
    }
    handledUsers.push(group1);
    handledUsers.push(group2);
    handledUsers.push(group3);
    handledUsers.push(group4);

    return handledUsers;
}
