import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "home",
            component: HomeView,
        },
        {
            path: "/booster/v1",
            name: "boosterV1",
            component: () => import("../components/Tasks.vue"),
        },
    ],
});

export default router;