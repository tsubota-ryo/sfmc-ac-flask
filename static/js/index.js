import Postmonger from 'postmonger';

/ JOURNEY BUILDER CUSTOM ACTIVITY - discountCode ACTIVITY
// ````````````````````````````````````````````````````````````
// This example demonstrates a custom activity that utilizes an external service to generate
// a discount code where the user inputs the discount percent in the configuration.
//
// Journey Builder's Postmonger Events Reference can be found here:
// https://developer.salesforce.com/docs/atlas.en-us.noversion.mc-app-development.meta/mc-app-development/using-postmonger.htm


// Custom activities load inside an iframe. We'll use postmonger to manage
// the cross-document messaging between Journey Builder and the activity
import Postmonger from 'postmonger';


// Create a new connection for this session.
// We use this connection to talk to Journey Builder. You'll want to keep this
// reference handy and pass it into your UI framework if you're using React, Angular, Vue, etc.
const connection = new Postmonger.Session();


// we'll store the activity on this variable when we receive it
let activity = null;


// Wait for the document to load before we doing anything
document.addEventListener('DOMContentLoaded', function main() {

    // Setup a test harness so we can interact with our custom activity
    // outside of journey builder using window functions & browser devtools.
    // This isn't required by your activity, its for example purposes only
    setupExampleTestHarness();

    // setup our ui event handlers
    setupEventHandlers();

    // Bind the initActivity event...
    // Journey Builder will respond with "initActivity" after it receives the "ready" signal
    connection.on('initActivity', onInitActivity);


    // We're all set! let's signal Journey Builder
    // that we're ready to receive the activity payload...

    // Tell the parent iFrame that we are ready.
    connection.trigger('ready');
});