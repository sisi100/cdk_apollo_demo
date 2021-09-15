exports.handler = async (event) => {
    console.log(event);
        let response = {
            "isAuthorized": true,
            "context": {}
        };
    return response
};
