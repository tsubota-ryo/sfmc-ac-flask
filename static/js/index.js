// JOURNEY BUILDER CUSTOM ACTIVITY - discountCode ACTIVITY
// ````````````````````````````````````````````````````````````
// This example demonstrates a custom activity that utilizes an external service to generate
// a discount code where the user inputs the discount percent in the configuration.
//
// Journey Builder's Postmonger Events Reference can be found here:
// https://developer.salesforce.com/docs/atlas.en-us.noversion.mc-app-development.meta/mc-app-development/using-postmonger.htm


const connection = new Postmonger.Session();


// we'll store the activity on this variable when we receive it
let activity = null;


// Wait for the document to load before we doing anything
document.addEventListener('DOMContentLoaded', function main() {

    setupEventHandlers();

    // Bind the initActivity event...
    // Journey Builder will respond with "initActivity" after it receives the "ready" signal
    connection.on('initActivity', onInitActivity);

    // Tell the parent iFrame that we are ready.
    connection.trigger('ready');
});

function onInitActivity(payload) {

    // set the activity object from this payload. We'll refer to this object as we
    // modify it before saving.
    activity = payload;

    const hasInArguments = Boolean(
        activity.arguments &&
        activity.arguments.execute &&
        activity.arguments.execute.inArguments &&
        activity.arguments.execute.inArguments.length > 0
    );

    const inArguments = hasInArguments ? activity.arguments.execute.inArguments : [];

    console.log('-------- triggered:onInitActivity({obj}) --------');
    console.log('activity:\n ', JSON.stringify(activity, null, 4));
    console.log('Has In Arguments: ', hasInArguments);
    console.log('inArguments', inArguments);
    console.log('-------------------------------------------------');

}

function onDoneButtonClick() {
    // we set must metaData.isConfigured in order to tell JB that
    // this activity is ready for activation
    activity.metaData.isConfigured = true;

    // get the option that the user selected and save it to

    const content_id = document.querySelector("#content_id").value;

    //TODO: データエクステンション名に応じ変更する
    activity.arguments.execute.inArguments = [{
        content_id: content_id,
        contact_key: "{{Contact.Key}}",
        uid: "{{Contact.Attribute.D1_TEST_user.UID}}",
        acid: "{{Contact.Attribute.D1_TEST_user.ACID}}",
        name: "{{Contact.Attribute.D1_TEST_user.name}}",
        campaign_id: "{{Contact.Attribute.D1_TEST_user.campaign_id}}"
    }];

    // you can set the name that appears below the activity with the name property
    activity.name = `${activity.arguments.execute.inArguments[0].content_id}`;

    console.log('------------ triggering:updateActivity({obj}) ----------------');
    console.log('Sending message back to updateActivity');
    console.log('saving\n', JSON.stringify(activity, null, 4));
    console.log('--------------------------------------------------------------');

    connection.trigger('updateActivity', activity);
}

function onCancelButtonClick() {
    // tell Journey Builder that this activity has no changes.
    // we wont be prompted to save changes when the inspector closes
    connection.trigger('setActivityDirtyState', false);

    // now request that Journey Builder closes the inspector/drawer
    connection.trigger('requestInspectorClose');
}

function setupEventHandlers() {
    // Listen to events on the form
    document.getElementById('done').addEventListener('click', onDoneButtonClick);
    document.getElementById('cancel').addEventListener('click', onCancelButtonClick);
}