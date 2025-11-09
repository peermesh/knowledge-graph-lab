import { ThemeProvider } from '../../shared/ThemeProvider'
import { SharedGraphLabPage } from '../../shared/pages/GraphLabPage'
import { iteration2Theme } from '../themeAdapter'

export function GraphLabPageV2() {
  return (
    <ThemeProvider theme={iteration2Theme}>
      <SharedGraphLabPage />
    </ThemeProvider>
  )
}












