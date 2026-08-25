export const metadata = {
  title: "Privacy Policy — History of Science Content Ops",
};

export default function PrivacyPage() {
  return (
    <main style={{ maxWidth: 720, margin: "40px auto", padding: 24, fontFamily: "system-ui", lineHeight: 1.5 }}>
      <h1>History of Science Content Ops — Privacy Policy</h1>
      <p>Last updated: 31 July 2026</p>
      <p>
        History of Science Content Ops stores account connection tokens and publishing metadata needed to upload
        videos on behalf of the channel operator. It is not a public consumer product.
      </p>
      <p>
        Connected platform credentials (for example TikTok OAuth tokens) are stored locally for
        publishing. We do not sell personal data. Session and publishing logs may include platform
        account identifiers required for API calls.
      </p>
      <p>
        For TikTok account data handled under Login Kit / Content Posting API, processing follows
        TikTok&apos;s developer terms and the operator&apos;s channel ownership.
      </p>
      <p>Contact: the channel operator via the History of Science YouTube channel.</p>
    </main>
  );
}
