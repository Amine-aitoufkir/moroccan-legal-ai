import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Moroccan Legal AI",
  description: "Assistant juridique marocain en cours de developpement",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="fr" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
