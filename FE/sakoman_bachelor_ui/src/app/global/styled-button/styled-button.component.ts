import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-styled-button',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './styled-button.component.html',
  styleUrl: './styled-button.component.scss'
})
export class StyledButtonComponent {
  @Input({ required: true}) icon: string = '';
  @Input({ required: true}) label: string = '';
  @Input() isClosing: boolean = false;

  @Output() clicked: EventEmitter<void> = new EventEmitter<void>();

  onClick(): void {
    this.clicked.emit();
  }
}
