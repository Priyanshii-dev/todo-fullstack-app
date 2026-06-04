import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

const HOME_ROUTE = "/";
const LOGIN_ROUTE = "/login";
const TASKS_ROUTE = "/tasks";
const ADMIN_LOGIN_ROUTE = "/admin/login";
const PUBLIC_ROUTES = [LOGIN_ROUTE, "/register"] as const;
const PRIVATE_ROUTES = [TASKS_ROUTE] as const;
const ADMIN_ROUTES = ["/admin/users"] as const;

function isRouteMatch(pathname: string, routes: readonly string[]) {
  return routes.some(
    (route) =>
      pathname === route ||
      pathname.startsWith(`${route}/`),
  );
}

/**
 * Proxy to handle route protection and redirection
 * based on authentication state.
 *
 * Next.js 16+: Middleware is renamed to Proxy.
 */
export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check authentication
  const accessToken = request.cookies.get("accessToken")?.value;
  const isAuthenticated = !!accessToken;

  // Route checks
  const isPublicRoute = isRouteMatch(pathname, PUBLIC_ROUTES);
  const isPrivateRoute = isRouteMatch(pathname, PRIVATE_ROUTES);
  const isAdminRoute = isRouteMatch(pathname, ADMIN_ROUTES);

  /**
   * Admin route protection — checked first to avoid
   * conflicts with general auth logic below.
   */
  if (isAdminRoute) {
    const adminToken = request.cookies.get("adminToken")?.value;
    if (!adminToken) {
      return NextResponse.redirect(new URL(ADMIN_LOGIN_ROUTE, request.url));
    }
  }

  /**
   * If authenticated user visits public routes
   * redirect them to tasks/dashboard.
   */
  if (isAuthenticated) {
    if (pathname === HOME_ROUTE || isPublicRoute) {
      return NextResponse.redirect(new URL(TASKS_ROUTE, request.url));
    }
  }

  /**
   * If unauthenticated user visits private routes
   * redirect to login page.
   */
  if (!isAuthenticated && isPrivateRoute) {
    const loginUrl = new URL(LOGIN_ROUTE, request.url);

    // Save original destination
    loginUrl.searchParams.set("callbackUrl", pathname);

    return NextResponse.redirect(loginUrl);
  }

  // Continue request
  return NextResponse.next();
}

/**
 * Routes handled by proxy
 */
export const config = {
  matcher: [
    /*
     * Match all routes except:
     * - api
     * - static files
     * - image optimization
     * - metadata files
     */
    "/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)",
  ],
};