import ProfileCard from "@/components/ProfileCard";

export default async function ProfilePage({ params }: { params: Promise<{ handle: string }> }) {
  const { handle } = await params;
  const res = await fetch(`http://localhost:8000/api/v1/profile/${handle}`, {
    next: { revalidate: 60 } // Next.js cache — matches your backend 60s cache
  });

  if (!res.ok) return <div>Profile not found</div>;
  const profile = await res.json();

  return (
    <main className="min-h-screen bg-zinc-950 flex items-center justify-center">
      <ProfileCard profile={profile} />
    </main>
  );
}
