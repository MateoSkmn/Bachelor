import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-star-evaluation',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './star-evaluation.component.html',
  styleUrl: './star-evaluation.component.scss'
})
export class StarEvaluationComponent {
  @Input() filledStars = 0;
  @Input() isInteractable = true;
  @Input() numberOfStars = 5;

  @Output() filledStarsChanged = new EventEmitter<number>();

  stars = Array(this.numberOfStars);

  /**
   * @param index Value to check which star was clicked
   */
  clickStar(index: number) {
    if (!this.isInteractable) {
      return
    }
    this.filledStars = index + 1;
    this.filledStarsChanged.emit(this.filledStars);
  }
}
