import Link from "next/link";
import { AffiliateImportForm } from "@/components/affiliate/AffiliateImportForm";

export const dynamic = "force-dynamic";

export default function AffiliateImportPage() {
  return (
    <div className="space-y-8">
      <div>
        <Link href="/affiliate" className="text-sm text-[#5A6E82] hover:text-[#F5E8D2]">
          ← Affiliate
        </Link>
        <h1 className="mt-2 font-[family-name:var(--font-orbit-display)] text-3xl">
          Conversion import
        </h1>
        <p className="mt-2 text-sm text-[#F5E8D2]/55">
          Import Amazon / Brilliant / generic affiliate reports. Preview before commit.
        </p>
      </div>
      <AffiliateImportForm />
      <div className="card-panel p-5 text-sm text-[#F5E8D2]/55">
        Sample CSV: <code>content/samples/csv/affiliate_amazon_sample.csv</code>
      </div>
    </div>
  );
}
