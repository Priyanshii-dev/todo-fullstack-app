importScripts(
  "https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js"
);

importScripts(
  "https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js"
);

firebase.initializeApp({
  apiKey: "AIzaSyAmaubpHT7ppIfiZ1YniXlg49HeNmg4dbs",
  authDomain: "to-do-19077.firebaseapp.com",
  projectId: "to-do-19077",
  storageBucket: "to-do-19077.firebasestorage.app",
  messagingSenderId: "67997603739",
  appId: "1:67997603739:web:5dcb3573c5f3bd2d82f33e",
  measurementId: "G-EZ9WSBJ0RQ",
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  self.registration.showNotification(
    payload.notification.title,
    {
      body: payload.notification.body,
    }
  );
});