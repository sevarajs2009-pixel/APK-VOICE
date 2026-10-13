// firebase-config.js

import { initializeApp } from "https://www.gstatic.com/firebasejs/12.19.0/firebase-app.js";

import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/12.19.0/firebase-auth.js";

import {
  getFirestore
} from "https://www.gstatic.com/firebasejs/12.19.0/firebase-firestore.js";


  const firebaseConfig = {
    apiKey: "AIzaSyAlGylt_DZL19Tm1HiXLTvJiT4BsHcVEcQ",
    authDomain: "voicetopara.firebaseapp.com",
    projectId: "voicetopara",
    storageBucket: "voicetopara.firebasestorage.app",
    messagingSenderId: "310577408579",
    appId: "1:310577408579:web:7594d39306dba23fe682f6",
    measurementId: "G-H5TXT48EH4"
  };


const app = initializeApp(firebaseConfig);


// Firebase Authentication
const auth = getAuth(app);

const googleProvider = new GoogleAuthProvider();


// Cloud Firestore
const db = getFirestore(app);


export {
  app,
  auth,
  db,
  googleProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged
};