import { PrismaClient } from "../../generated/prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";

/**
 * Prisma client singleton — safe for Vercel serverless.
 * Cache on globalThis so warm lambdas reuse one client (avoids connection storms).
 */
const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    adapter: new PrismaPg({
      connectionString: process.env.DATABASE_URL,
      connectionTimeoutMillis: 5000,
      idleTimeoutMillis: 300000,
    }),
    log: process.env.NODE_ENV === "development" ? ["error", "warn"] : ["error"],
  });

globalForPrisma.prisma = prisma;
