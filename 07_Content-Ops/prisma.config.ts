import "dotenv/config";
import { defineConfig } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: { path: "prisma/migrations", seed: "tsx prisma/seed.ts" },
  // Migrations must use the direct connection when one is supplied.
  // Generation remains possible without any database credentials.
  datasource: { url: process.env.DIRECT_URL || process.env.DATABASE_URL || "" },
});
