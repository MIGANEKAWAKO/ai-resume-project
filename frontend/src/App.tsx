import { Toaster } from "sonner"
import { Header } from "@/components/Header"
import { HomePage } from "@/pages/HomePage"

export default function App() {
  return (
    <div className="min-h-screen bg-[var(--color-background)]">
      <Header />
      <HomePage />
      <Toaster position="top-right" richColors closeButton />
    </div>
  )
}
