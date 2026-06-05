import { getToken } from "firebase/messaging";
import { messaging } from "./firebase-messaging";

export async function requestNotificationPermission() {
  try {
    const permission =
      await Notification.requestPermission();

    if (permission !== "granted") {
      console.log("Notification permission denied");
      return null;
    }

    const token = await getToken(
      messaging!,
      {
        vapidKey:
          process.env.NEXT_PUBLIC_FIREBASE_VAPID_KEY,
      }
    );

    console.log("FCM Token:", token);

    return token;
  } catch (error) {
    console.error(error);
    return null;
  }
}