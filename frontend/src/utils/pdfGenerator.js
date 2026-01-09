import jsPDF from 'jspdf'
import { RobotoRegularFont } from '../fonts/Roboto-Regular.js'

// Page sizes in points (1 point = 1/72 inch)
const PAGE_SIZES = {
  A4: [595.28, 841.89],      // 210 x 297 mm
  LETTER: [612, 792]          // 8.5 x 11 inches
}

/**
 * Apply text case transformation
 */
function applyCase(text, caseMode) {
  switch (caseMode) {
    case 'upper':
      return text.toUpperCase()
    case 'lower':
      return text.toLowerCase()
    case 'sentence':
      return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase()
    default:
      return text
  }
}

/**
 * Calculate slots for phrases on a page
 */
function makeSlots(pageW, pageH, margin, phrasesPerPage, gutter) {
  const usableW = pageW - 2 * margin
  const usableH = pageH - 2 * margin

  if (usableW <= 0 || usableH <= 0) {
    throw new Error('Margins too large for the selected page size')
  }

  const slots = []

  if (phrasesPerPage === 1) {
    slots.push([margin, margin, usableW, usableH])
  } else if (phrasesPerPage === 2) {
    const slotH = (usableH - gutter) / 2
    if (slotH <= 0) throw new Error('Gutter too large')
    // Top then bottom (PDF coordinates: bottom-left origin)
    slots.push([margin, margin + slotH + gutter, usableW, slotH])
    slots.push([margin, margin, usableW, slotH])
  } else if (phrasesPerPage === 4) {
    const slotW = (usableW - gutter) / 2
    const slotH = (usableH - gutter) / 2
    if (slotW <= 0 || slotH <= 0) throw new Error('Gutter too large')
    
    const leftX = margin
    const rightX = margin + slotW + gutter
    const bottomY = margin
    const topY = margin + slotH + gutter
    
    slots.push(
      [leftX, topY, slotW, slotH],
      [rightX, topY, slotW, slotH],
      [leftX, bottomY, slotW, slotH],
      [rightX, bottomY, slotW, slotH]
    )
  }

  return slots
}

/**
 * Draw cut guides
 */
function drawGuides(pdf, mode, x, y, w, h) {
  if (mode === 'none') return

  pdf.setDrawColor(180, 180, 180)
  pdf.setLineWidth(0.5)

  // Draw box around the phrase
  if (mode === 'box' || mode === 'all') {
    pdf.rect(x, y, w, h)
  }

  // Draw internal cut lines at 1/3 and 2/3
  if (mode === 'internal' || mode === 'all') {
    const yTopCut = y + h * (2 / 3)
    const yBotCut = y + h * (1 / 3)
    pdf.line(x, yTopCut, x + w, yTopCut)
    pdf.line(x, yBotCut, x + w, yBotCut)
  }
}

/**
 * Fit text to width and height constraints
 */
function fitFontSize(pdf, text, maxSize, minSize, maxW, maxH) {
  let size = maxSize
  
  while (size >= minSize) {
    pdf.setFontSize(size)
    const textWidth = pdf.getTextWidth(text)
    
    // Check if text fits both width and height
    if (textWidth <= maxW && size <= maxH) {
      return size
    }
    size -= 1
  }
  
  return minSize
}

/**
 * Draw text centered with optional horizontal scaling
 */
function drawCenteredScaled(pdf, text, cx, cy, fontSize, maxWidth) {
  pdf.setFontSize(fontSize)
  const textWidth = pdf.getTextWidth(text)
  
  if (textWidth <= maxWidth) {
    // Text fits, draw normally
    pdf.text(text, cx, cy, { align: 'center', baseline: 'middle' })
  } else {
    // Scale horizontally to fit
    const scale = maxWidth / textWidth
    pdf.saveGraphicsState()
    pdf.text(text, cx, cy, { 
      align: 'center', 
      baseline: 'middle',
      charSpace: -fontSize * (1 - scale) * 0.1  // Approximate scaling via char spacing
    })
    pdf.restoreGraphicsState()
  }
}

/**
 * Main PDF generation function
 */
export async function generateFlipBookPDF(phrases, config) {
  const {
    pageSize = 'A4',
    phrasesPerPage = 1,
    cutGuides = 'internal',
    textCase = 'none',
    maxFont = 110,
    minFont = 26,
    margin = 48,
    padding = 18,
    gutter = 18
  } = config

  // Get page dimensions
  const [pageW, pageH] = PAGE_SIZES[pageSize] || PAGE_SIZES.A4

  // Create PDF - jsPDF uses different coordinate system than ReportLab
  // jsPDF origin is top-left, we'll convert coordinates
  const orientation = pageW > pageH ? 'landscape' : 'portrait'
  const pdf = new jsPDF({
    orientation,
    unit: 'pt',
    format: [pageW, pageH]
  })

  // Add Roboto font with Cyrillic support
  pdf.addFileToVFS('Roboto-Regular.ttf', RobotoRegularFont)
  pdf.addFont('Roboto-Regular.ttf', 'Roboto', 'normal')
  pdf.setFont('Roboto')

  const slots = makeSlots(pageW, pageH, margin, phrasesPerPage, gutter)
  let idx = 0
  const total = phrases.length

  while (idx < total) {
    if (idx > 0) {
      pdf.addPage()
    }

    for (const [x, yBottom, w, h] of slots) {
      if (idx >= total) break

      const phrase = phrases[idx]
      const lines = [
        applyCase(phrase.a, textCase),
        applyCase(phrase.b, textCase),
        applyCase(phrase.c, textCase)
      ]

      // Calculate inner dimensions
      const innerX = x + padding
      const innerY = yBottom + padding
      const innerW = Math.max(1, w - 2 * padding)
      const innerH = Math.max(1, h - 2 * padding)
      const thirdH = innerH / 3

      // Convert from bottom-left origin to top-left origin for jsPDF
      const yTop = pageH - yBottom - h

      // Calculate y positions for three lines (in jsPDF top-left coordinates)
      const centerX = innerX + innerW / 2
      
      // Top, middle, bottom line positions
      const yTopLine = yTop + padding + thirdH / 2
      const yMidLine = yTop + padding + innerH / 2
      const yBotLine = yTop + padding + innerH - thirdH / 2

      // Fit each line independently
      const sizes = [
        fitFontSize(pdf, lines[0], maxFont, minFont, innerW, thirdH),
        fitFontSize(pdf, lines[1], maxFont, minFont, innerW, thirdH),
        fitFontSize(pdf, lines[2], maxFont, minFont, innerW, thirdH)
      ]

      // Draw each line
      drawCenteredScaled(pdf, lines[0], centerX, yTopLine, sizes[0], innerW)
      drawCenteredScaled(pdf, lines[1], centerX, yMidLine, sizes[1], innerW)
      drawCenteredScaled(pdf, lines[2], centerX, yBotLine, sizes[2], innerW)

      // Draw guides (convert coordinates for drawing)
      drawGuides(pdf, cutGuides, x, yTop, w, h)

      idx++
    }
  }

  // Save the PDF
  const filename = `flip-n-giggle-${Date.now()}.pdf`
  pdf.save(filename)
  
  return filename
}
