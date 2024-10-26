import { WelcomeAbout } from "@features/WelcomeAbout"
import { WelcomeHero } from "@features/WelcomeHero"

export const WelcomePage = () => {
  return (
    <>
      <WelcomeHero />
      <WelcomeAbout />
    </>
  )
}