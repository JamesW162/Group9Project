// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyAEzhS9bkzcN5-YLuvta9Vm2aYM6DYl2PU", // Replace with your Firebase API key
    authDomain: "bsltranslator-93f00.firebaseapp.com",
    databaseURL: "https://bsltranslator-93f00-default-rtdb.europe-west1.firebasedatabase.app/",
    projectId: "bsltranslator-93f00",
    storageBucket: "bsltranslator-93f00.appspot.com",
    messagingSenderId: "547548973040", // Replace with your messaging sender ID
    appId: "1:547548973040:web:4c7b2802aedcf6e84a7f35" // Replace with your app ID
};
 
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const database = firebase.database();